#!/usr/bin/env python3
"""Gourmet Trails: find food photos in the Mac Photos library, group them into meals,
name the restaurant at each meal's location, export web-sized JPEGs, and tag the photos.

  photos.py scan   --from 2026-10-01 --to 2026-10-11 [--term food] [--no-lookup]
  photos.py export --out DIR ID [ID ...]
  photos.py tag    --keyword "Gourmet Trails" --keyword "<Restaurant name>" ID [ID ...]

Talks to the Photos app through AppleScript (macOS asks once to allow controlling Photos).
Restaurant lookups use OpenStreetMap (Nominatim reverse, Overpass nearby search).
"""
import argparse, json, math, os, shutil, subprocess, sys, tempfile, time, urllib.parse
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
BRIDGE = os.path.join(HERE, "photos.applescript")
UA = "gourmet-trails-plugin/1.0 (personal restaurant log; https://github.com/benchlog-ai/plugins)"
EATS = "restaurant|cafe|fast_food|bar|pub|biergarten|ice_cream|food_court"
TAG = "Gourmet Trails"


def osa(*args, timeout=600):
    r = subprocess.run(["osascript", BRIDGE, *args], capture_output=True, text=True, timeout=timeout)
    if r.returncode:
        sys.exit("Photos bridge failed: " + r.stderr.strip())
    return r.stdout


def num(s):
    s = (s or "").strip().replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def metres(a, b):
    dy = (a[0] - b[0]) * 111_320
    dx = (a[1] - b[1]) * 111_320 * math.cos(math.radians(a[0]))
    return math.hypot(dx, dy)


def get_json(url, data=None, timeout=40):
    # curl ships with macOS and uses the system certificates; python.org builds often lack them
    cmd = ["curl", "-sfS", "-m", str(timeout), "-A", UA, url]
    if data is not None:
        cmd[1:1] = ["--data-binary", data.decode()]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(r.stderr.strip() or f"curl exit {r.returncode}")
    return json.loads(r.stdout)


def reverse(lat, lon):
    q = urllib.parse.urlencode({"lat": lat, "lon": lon, "format": "jsonv2", "zoom": 18})
    try:
        d = get_json("https://nominatim.openstreetmap.org/reverse?" + q)
    except Exception as e:  # network or rate limit
        return {"error": str(e)}
    a = d.get("address", {})
    return {
        "name": d.get("name") or "",
        "kind": f'{d.get("category", "")}/{d.get("type", "")}',
        "address": " ".join(x for x in [a.get("house_number"), a.get("road")] if x),
        "area": a.get("suburb") or a.get("neighbourhood") or a.get("quarter") or "",
        "city": a.get("city") or a.get("town") or a.get("village") or "",
        "country": a.get("country_code", "").upper(),
    }


def nearby(lat, lon, radius=80):
    ql = f'[out:json][timeout:25];nwr(around:{radius},{lat},{lon})[amenity~"^({EATS})$"];out center tags;'
    body = urllib.parse.urlencode({"data": ql}).encode()
    for host in ("https://overpass-api.de/api/interpreter", "https://overpass.kumi.systems/api/interpreter"):
        try:
            d = get_json(host, data=body)
            break
        except Exception:
            continue
    else:
        return None  # both mirrors busy: the skill falls back to the reverse lookup and web search
    out = []
    for e in d.get("elements", []):
        t = e.get("tags", {})
        if not t.get("name"):
            continue
        la, lo = e.get("lat", e.get("center", {}).get("lat")), e.get("lon", e.get("center", {}).get("lon"))
        out.append({"name": t["name"], "amenity": t.get("amenity"), "cuisine": t.get("cuisine", ""),
                    "metres": round(metres((lat, lon), (la, lo)))})
    return sorted(out, key=lambda x: x["metres"])[:6]


def scan(a):
    f, t = a.date_from.replace("-", ""), a.date_to.replace("-", "")
    rows = []
    for line in osa("find", f, t, a.term).splitlines():
        p = line.split("\t")
        if len(p) < 5:
            continue
        rows.append({"id": p[0], "file": p[1], "at": p[2], "lat": num(p[3]), "lon": num(p[4]),
                     "keywords": [k for k in (p[5] if len(p) > 5 else "").split("|") if k]})
    rows.sort(key=lambda r: r["at"])

    meals = []
    for r in rows:
        when = datetime.fromisoformat(r["at"])
        m = meals[-1] if meals else None
        close_in_time = m and (when - m["_last"]).total_seconds() <= 3 * 3600
        here = r["lat"] is not None
        close_in_space = m and (not here or m["_pos"] is None or metres((r["lat"], r["lon"]), m["_pos"]) <= 150)
        if m and close_in_time and close_in_space:
            m["photos"].append(r)
            m["_last"] = when
            if here and m["_pos"] is None:
                m["_pos"] = (r["lat"], r["lon"])
        else:
            meals.append({"photos": [r], "_last": when, "_pos": (r["lat"], r["lon"]) if here else None})

    out = []
    for i, m in enumerate(meals, 1):
        pts = [(p["lat"], p["lon"]) for p in m["photos"] if p["lat"] is not None]
        pos = (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)) if pts else None
        first, last = m["photos"][0]["at"], m["photos"][-1]["at"]
        meal = {"meal": i, "date": first[:10], "from": first[11:16], "to": last[11:16],
                "count": len(m["photos"]),
                "already_tagged": all(TAG in p["keywords"] for p in m["photos"]),
                "lat": round(pos[0], 6) if pos else None, "lon": round(pos[1], 6) if pos else None,
                "photos": [{"id": p["id"], "file": p["file"], "at": p["at"]} for p in m["photos"]]}
        if pos and not a.no_lookup and not meal["already_tagged"]:
            meal["here"] = reverse(*pos)
            time.sleep(1.1)  # Nominatim allows one request per second
            meal["nearby"] = nearby(*pos)
        out.append(meal)
    json.dump({"from": a.date_from, "to": a.date_to, "term": a.term, "photos": len(rows),
               "meals": out}, sys.stdout, indent=1, ensure_ascii=False)
    print()


def export(a):
    try:
        from PIL import Image, ImageOps
    except ImportError:
        sys.exit("Pillow is needed: pip install --break-system-packages -q pillow")
    os.makedirs(a.out, exist_ok=True)
    done = []
    for n, pid in enumerate(a.ids, 1):
        tmp = tempfile.mkdtemp(prefix="gt-export-")
        try:
            osa("export", tmp, pid)
            files = [os.path.join(tmp, x) for x in os.listdir(tmp)]
            if not files:
                done.append({"id": pid, "error": "nothing exported (iCloud original not downloaded?)"})
                continue
            im = ImageOps.exif_transpose(Image.open(files[0])).convert("RGB")
            im.thumbnail((1400, 1400))
            dest = os.path.join(a.out, f"{n:02d}.jpg")
            im.save(dest, "JPEG", quality=82)  # a fresh JPEG carries no EXIF, so no GPS leaves the Mac
            done.append({"id": pid, "file": dest})
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    json.dump(done, sys.stdout, indent=1)
    print()


def tag(a):
    n = osa("tag", "|".join(a.keyword), *a.ids).strip()
    print(f"tagged {n} photos with: {', '.join(a.keyword)}")


ap = argparse.ArgumentParser()
sub = ap.add_subparsers(dest="cmd", required=True)
s = sub.add_parser("scan")
s.add_argument("--from", dest="date_from", required=True)
s.add_argument("--to", dest="date_to", required=True)
s.add_argument("--term", default="food")
s.add_argument("--no-lookup", action="store_true")
s.set_defaults(fn=scan)
e = sub.add_parser("export")
e.add_argument("--out", required=True)
e.add_argument("ids", nargs="+")
e.set_defaults(fn=export)
g = sub.add_parser("tag")
g.add_argument("--keyword", action="append", required=True)
g.add_argument("ids", nargs="+")
g.set_defaults(fn=tag)
args = ap.parse_args()
args.fn(args)

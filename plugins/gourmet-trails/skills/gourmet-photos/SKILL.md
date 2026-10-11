---
name: gourmet-photos
description: Scans the Mac Photos library for food photos, groups them into meals, names the restaurant from each meal's location, adds the meals to the user's Gourmet Trails page with captioned dish photos, and tags the photos in Photos with the restaurant's name. macOS only. Use when the user says "check my photos for restaurants", "scan my camera roll since September", "any new food photos this week?", "import last month's dinners from Photos", "tag my food photos", or "find the photos from La Esquina".
---

# Restaurants from the Mac Photos library

**Page first:** follow `${CLAUDE_PLUGIN_ROOT}/references/page-setup.md` to find or create the
user's Gourmet Trails page (PAGE). Data model:
`${CLAUDE_PLUGIN_ROOT}/skills/gourmet-log/references/data-model.md`. Dish captions, cover
choice and record writing follow `${CLAUDE_PLUGIN_ROOT}/skills/gourmet-log/references/photo-workflow.md`
(steps 5, 7–9).

**macOS only.** Runs on a Mac with the Photos app and `python3`. If the session is not on a
Mac (`uname` is not `Darwin`), say so in one line and offer the chat-upload route in
`gourmet-log` instead. The script talks to Photos through AppleScript; the first run makes
macOS ask the user to let Claude control Photos. Nothing is copied off the Mac except the
web-sized JPEGs that get uploaded to the page, and those carry no GPS. Restaurant lookups send
each meal's coordinates to OpenStreetMap (Nominatim and Overpass), and nothing else.

`P=${CLAUDE_PLUGIN_ROOT}/skills/gourmet-photos/scripts/photos.py`

Write temporary files to your scratchpad directory (`$TMP` below), or `/tmp` if there is none.

## Steps

1. **Pick the window.** From the user's words ("since September", "this week"); default to the
   30 days up to today. Long windows are fine; Photos' own search does the filtering.
2. **Scan.**
   ```bash
   python3 $P scan --from <YYYY-MM-DD> --to <YYYY-MM-DD> > $TMP/gt-scan.json
   ```
   This uses Photos' built-in "food" search (Apple's on-device recognition), groups photos into
   meals (same place within ~150 m, gaps under 3 h), and for each untagged meal returns `here`
   (the OpenStreetMap place at the spot) and `nearby` (named restaurants, cafés and bars within
   80 m, nearest first). `--term` changes the search ("dessert", "drinks"). Meals with
   `already_tagged: true` were imported before: skip them.
3. **Name each meal's restaurant.**
   - `here.kind` is `amenity/restaurant` (or cafe, fast_food, bar…) and the name matches a
     `nearby` entry within ~40 m: confident. Use it.
   - Several `nearby` candidates and no clear winner: look at one or two photos (export them,
     step 4) for coasters, menus or plates with a name, and web-search the candidates' menus
     against the dishes you see.
   - `here.kind` is a house, residential or office address and `nearby` is empty: home cooking
     or a friend's place. Skip it without comment. **Never** write, repeat or display that
     address or the coordinates anywhere.
   - No GPS: group it into one question for the user at the end ("Which restaurant was the
     12 Sept lunch with ramen?").
   Match the name against `places` (list it first). An existing place gets a new visit; a new
   one is created as visited, with `source: "Photos library"`.
4. **Export the photos of each meal you are adding** (up to 25 per call):
   ```bash
   pip install --break-system-packages -q pillow 2>/dev/null
   python3 $P export --out $TMP/gt-<slug> <id> <id> …
   ```
   Files come out as `01.jpg, 02.jpg …` at 1400 px, EXIF-free, in the order of the ids. Look at
   each one: drop non-dishes (menus, people, receipts, blurred shots) and pick 3–8 per meal.
   Never upload a photo where a person is the subject.
5. **Upload and write**: `Artifact` with `url` = PAGE, `asset: true` and `file_paths`, then
   append `photos`, `dishes`, `visits` (date = meal date) and set `lastVisit`, per
   `data-model.md`. Leave `rating` and `note` alone; ask for a rating in the summary instead.
6. **Tag in Photos**, so the library shows the same names as the page:
   ```bash
   python3 $P tag --keyword "Gourmet Trails" --keyword "<Restaurant name>" <every id in the meal>
   ```
   Tag all of the meal's photos (also the ones not uploaded), so the next scan skips them.
   Keywords only add; existing ones stay. In Photos, the user can then search the
   restaurant's name.
7. **Report in a few lines**: meals found, places added or updated, photos uploaded, meals
   skipped as home or already imported (counts only), names still needed, and one ask:
   "Ratings 1–5 for the new ones?".

## Judgement

- A wrong name is worse than a question. Say how sure you are when it isn't the `here` match.
- Places close down and move: confirm a new place on the web before creating it.
- The first scan of a long period can return dozens of meals. Do the confident ones, then ask
  about the rest in one message.
- If macOS refuses control of Photos, tell the user where to allow it (System Settings ›
  Privacy & Security › Automation) and stop; don't try another route into the library.

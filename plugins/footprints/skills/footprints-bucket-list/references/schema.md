# Footprints data reference

## The page

- Title: "Footprints". Get its URL with the find-or-create step in `${CLAUDE_PLUGIN_ROOT}/references/page-setup.md` (it creates the user's private page on first run).
- Read and write with the `ArtifactData` tool (load it with ToolSearch `select:ArtifactData` if it is deferred). Every call takes that page URL.
- Writes to an existing document need `if_version` from your last read. Use one `batch` (max 50 writes) whenever you change more than two documents.
- Everything you write appears on the page live. Never write `example: true`; that flag marks sample data the user can clear.

## Who sees what

The page can be shared. Access rules are fixed:

| Collection | Shared viewers | Owner |
|---|---|---|
| `places`, `bucket`, `photos` | read | read and write |
| `notes`, `trips`, `profile` | hidden | read and write |

So anything personal (who the user travelled with, private memories, costs, booking references, plans) goes in `notes`, `trips` or `profile`, never in a `places` caption or a `bucket` note. Captions are written to be shown to friends.

## Home location

The user's home city and departure airport live in `profile/travel.home`. Nothing is assumed: there is no default home.

- Any skill that needs home (flight arcs, distances, flight searches, "from home" wording, public holidays) reads `profile/travel` first.
- If `home` is missing, ask once, in one short question: "Which city do you usually travel from, and which airport do you fly out of?" Then save it before continuing: `set` `profile/travel` if the document doesn't exist, otherwise `update` it with `if_version`. Fill `lat`/`lng` from well-known city coordinates, `code` from the airport's IATA code, and `country` (plus `region` if they mention a state or canton, since public holidays often differ by region). Add `currency` if they mention one or it is obvious from the country, and say what you assumed.
- If the user declines, carry on without home: skip arcs-from-home and distance claims, and ask for a departure airport only when a flight search needs it.

## Collections

### `places/{id}` — Visited pins (public)

| Field | Type | Notes |
|---|---|---|
| `name` | string | City or place as the user says it ("Porto", "Isle of Skye") |
| `country` | string | Plain country name. The map tints the country containing the pin; the name is a fallback. |
| `lat`, `lng` | number | Decimal degrees, 4 places. Use the city centre or the named spot. Required for a pin. |
| `from`, `to` | string | `YYYY-MM-DD`, or `YYYY-MM` / `YYYY` when only that is known. `to` may be empty. |
| `caption` | string | One shareable line, max 220 chars, in the user's voice. |
| `highlights` | string[] | Short phrases, 0–6. |
| `tags` | string[] | Lowercase. Prefer: city, coast, islands, mountains, snow, desert, forest, lakes, ruins, food, photography, hiking, temples, culture, nightlife, road trip, wildlife. |
| `rating` | number or null | 1–5, only if the user gave one. |
| `photoId` | string or null | Id in `photos`. Leave null unless a photo was stored. |
| `updated` | string | ISO timestamp. |

Doc id: lowercase slug of name plus year, e.g. `porto-2024`. Add `-2` for a repeat visit in the same year. A repeat visit to a place in a different year is its own pin.

### `notes/{placeId}` — Private memories (same id as the place)

`memory` (free text, the user's words), `with` (who came), `food` (dishes and spots worth remembering). All strings.

### `bucket/{id}` — Bucket list (public)

| Field | Type | Notes |
|---|---|---|
| `name`, `country` | string | |
| `lat`, `lng` | number or null | Approximate is fine. |
| `why` | string | One or two sentences of why the user wants to go. |
| `season` | string | Best months, e.g. "Feb – Mar". |
| `priority` | 1, 2 or 3 | 1 = Next up, 2 = Soon, 3 = Someday. |
| `scene` | string | Drives the illustrated postcard: one of `mountains`, `coast`, `city`, `desert`, `forest`, `islands`, `snow`, `lakes`, `ruins`. Pick what the place is famous for. |
| `tags` | string[] | Same vocabulary as places. |
| `photoId` | string or null | Only set by the page when the user uploads a photo. |
| `added` | string | `YYYY-MM-DD`. |

The page draws each postcard itself; it cannot load photos from the web, so never write image URLs.

### `photos/{id}` — Uploaded images

Written by the page only (`{data: "data:image/jpeg;base64,…", of: "places/<id>"}`). Do not create or edit these; delete one only together with the place or bucket item that owns it.

### `trips/{id}` — Plans (private)

| Field | Type | Notes |
|---|---|---|
| `title` | string | Short, e.g. "Marrakech & the Atlas". |
| `destination` | string | "City, Country" or a region. |
| `status` | string | `brainstorm` → `planning` → `booked` → `done`. |
| `start`, `end` | string | `YYYY-MM-DD`, empty while dates are open. |
| `budget` | string | As the user stated it, e.g. "€900". |
| `summary` | string | Two or three sentences: the shape of the trip and why it suits the user. |
| `bucketId` | string or null | The bucket item this came from. |
| `days` | array | See below. |
| `packing` | array | `{id, item, group, qty?, done}`. Groups: Documents, Clothes, Photo, Tech, Toiletries, Health, Other. Keep `done` values when rewriting. |
| `tickets` | array | `{id, kind, title, detail, when, price, currency, status, bookBy?, ref?, link?}`. `kind`: flight, train, stay, car, activity, insurance, other. `status`: `to-book` or `booked`. `price` is a number. `currency` defaults to `profile.currency` when the price was quoted in it. Keep `status` and `ref` when rewriting. |
| `created` | string | ISO timestamp. |

`days[]`: `{date: "YYYY-MM-DD", title, base, items: [{time: "HH:MM" or "", kind, title, note}]}`. Item `kind` picks the icon: flight, train, car, stay, sight, food, photo, hike, rest, activity, other. Keep each note to one line.

The page lets the user tick packing items, toggle tickets between `to-book` and `booked`, add packing items (group "Added") and change the status. Read the trip right before rewriting it so those edits survive.

### `profile/travel` — Travel profile (private, one document)

| Field | Type |
|---|---|
| `home` | `{name, country, region?, lat, lng, code}` — the user's home city and departure airport IATA code. No default; see "Home location". |
| `currency` | string, optional (symbol or ISO code the user budgets in, e.g. "€", "GBP") |
| `pace` | string (e.g. "slow, 2–3 things a day") |
| `budget` | string (typical per-trip range in the user's words) |
| `interests` | string[] |
| `food` | string |
| `photography` | string (what they shoot, gear they bring) |
| `climate` | string (likes and dislikes) |
| `companions` | string |
| `tripLength` | string (e.g. "long weekends plus two 1-week trips a year") |
| `avoid` | string[] (things the user doesn't want: overtouristy, long-haul over 12h, etc.) |
| `constraints` | string (passport, visas, vacation days, dates they can't travel) — useful for planning, never shown on shared views |
| `notes` | string |
| `updated` | ISO timestamp |

Only write what the user actually said. Never invent a preference.

## Lookups

- **Coordinates:** use well-known city coordinates. If unsure of a small place, search the web for "<place> coordinates" and use the first authoritative value.
- **Country for the map:** the page detects the country from `lat`/`lng`, so coordinates matter more than spelling.
- **Distances:** great-circle from `profile.home`. No home saved means no distance claims.

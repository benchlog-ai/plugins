# Gourmet Trails data model

The page is the user's own private artifact titled **"Gourmet Trails"** (PAGE). Find or create
it with `${CLAUDE_PLUGIN_ROOT}/references/page-setup.md`.
All records live in that artifact's database. Read and write them with the `ArtifactData` tool
(`url` = PAGE). Photos live in the artifact's asset store (Artifact tool, `url` = PAGE,
`asset: true`). Never republish the page HTML to change data; the page re-renders from the
database live.

## Collection `places` (one document per restaurant)

Document id: a lowercase slug of the name (`saffron-house`, `hoshi-izakaya`). For a place whose
name is not known yet, use `<cuisine-or-dish>-unnamed` and set `needsName: true`.

| Field | Type | Meaning |
|---|---|---|
| `name` | string | Restaurant name as the user or the venue writes it. Placeholder like "Tapas restaurant" while `needsName` is true. |
| `needsName` | bool | True until the user confirms which restaurant it is. The page shows a "Name needed" badge. |
| `status` | `"visited"` \| `"wishlist"` | Been there vs Want to go. |
| `cuisine` | string | One label, title case, consistent across places: "South Indian", "Spanish", "Japanese", "Brunch", "Turkish". Reuse an existing label before inventing a new one (list the collection first). Passport stamps are built from this field. |
| `area` | string | Neighbourhood ("Old Town", "Riverside"). |
| `city` | string | The city the place is in. The page builds its city filter from this. |
| `address` | string | Street address when known. |
| `mapsUrl` | string | A Google Maps link. Use the link the user pasted, or `https://www.google.com/maps/search/?api=1&query=<url-encoded name, address>`. |
| `order` | string | The headline dish: what to order here. Shown as "Order …… dish" and on share cards. |
| `dishes` | string[] | Dishes the user has had here (visited). |
| `toTry` | string[] | 2–3 dishes to try (wishlist). First one is "order first". |
| `rating` | int 0–5 | The user's rating. 0 means not rated. Only the user sets it (in chat or on the page). Never guess one. |
| `note` | string | One short sentence in the user's words. Leave empty rather than inventing a note. |
| `photos` | `{id,url,dish}[]` | Asset id, the `/_blob/<id>` url exactly as the upload returned it, and a short dish caption. |
| `cover` | int | Index into `photos` used as the card cover. |
| `visits` | `{date, note?}[]` | One entry per visit; `date` is `YYYY-MM-DD` or omitted when unknown. |
| `lastVisit` | string | Latest visit date (`YYYY-MM-DD`). Drives "Recent" sort. |
| `source` | string | Provenance: "Google Maps link", "Added by name", "Photos", "Photos library", "From <friend>", "Suggested by Claude". |
| `by` | string | Friend who recommended it (wishlist). Page shows "From <by>". |
| `priceBand` | string | Optional: one to three symbols in the user's currency ("€", "$$", "£££"). |
| `createdAt`, `updatedAt` | ISO string | Set both on create; update `updatedAt` on every change. |

## Collection `lists` (Best of collections)

Document id: slug of the title (`best-of-brunch`).

| Field | Type | Meaning |
|---|---|---|
| `title` | string | "Best of brunch", "My Italian top 5". |
| `note` | string | One line shown under the title. |
| `placeIds` | string[] | Ordered `places` document ids. |
| `createdAt`, `updatedAt` | ISO string | |

## Document `meta/profile` (taste profile)

Collection `meta`, doc id `profile`. Written by onboarding, read by recommendations and share
cards. The page reads `name` for its header and share card.

| Field | Type |
|---|---|
| `name` | string, optional: first name or handle shown on share cards and the page header ("Maya recommends"). Empty → "Recommended". |
| `loves` | string[] cuisines or dishes the user loves |
| `avoid` | string[] things they do not eat or dislike (dietary choices only, as they state them) |
| `spice` | string ("loves heat", "medium") |
| `budget` | string ("mid-range most nights, splurge for occasions") |
| `companions` | string (who they usually eat with, e.g. "usually with a partner") |
| `occasions` | string[] ("weekday lunch near work", "weekend brunch") |
| `homeBase` | string (city and neighbourhood they eat around, e.g. "lives in the north of the city, works downtown") |
| `notes` | string |
| `updatedAt` | ISO string |

Do not store health conditions or allergies here; if the user mentions one, use it in the
conversation only.

## Writing rules

- Read before writing: `list`/`get` first, then pass each document's `version` as `if_version`
  (in a batch, per entry). Creating a new document needs no version.
- Use `update` (merge) for edits; send whole arrays (`photos`, `dishes`, `visits`) with the new
  item appended, built from the version you just read.
- Use one `batch` when writing more than two documents.
- Before adding a place, check for an existing document with the same or a similar name
  (also check `needsName` placeholders with the same cuisine) to avoid duplicates. Merge into it.
- After writing, open the page with `Artifact` `action: "open"` only when the user should look
  now.

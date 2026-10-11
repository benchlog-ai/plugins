# Wardrobe data model

All data lives in the shared database of the user's private **Wardrobe** page (find or create it with `${CLAUDE_PLUGIN_ROOT}/references/page-setup.md`).

Read and write it with the `ArtifactData` tool (load it with ToolSearch `select:ArtifactData` if deferred). The page renders `items`, `outfits`, `combos`, `outfit_ideas` and `suggestions`, so keep the names and value formats. `events` and `profile` are kept for the skills and not shown on the page.

## `items` — one document per wardrobe piece or accessory

Doc id: kebab-case slug of the name, e.g. `navy-wool-blazer`. Add `-2`, `-3` if the slug exists.

| Field | Type | Notes |
|---|---|---|
| `name` | string | Short, human name: "Navy wool blazer" |
| `category` | string | One of `top`, `bottom`, `outerwear`, `suit`, `traditional`, `footwear`, `accessory` |
| `subtype` | string | e.g. shirt, blouse, polo, t-shirt, chinos, jeans, skirt, dress, kurta, sherwani, saree, lehenga, loafers, heels, watch, belt, tie, pocket square, bag, sunglasses |
| `color_name` | string | Plain color name, title case: "Navy", "Olive", "Off-white", "Burgundy" |
| `hex` | string | Main color as `#RRGGBB` (always 6 digits) |
| `secondary_hex` | string, optional | Second color for patterned/two-tone pieces |
| `pattern` | string | `solid`, `stripe`, `check`, `herringbone`, `print`, `textured`, … |
| `fabric` | string, optional | wool, cotton, linen, denim, leather, silk, knit |
| `formality` | number 1–5 | 1 = loungewear, 2 = casual, 3 = smart casual, 4 = business, 5 = black tie / ceremonial |
| `seasons` | string[] | Any of `spring`, `summer`, `autumn`, `winter`, `all` |
| `occasions` | string[] | Lowercase event tags: `office`, `casual`, `date`, `wedding`, `formal`, `travel`, `party`, `sport`, `festival` |
| `pairs_with` | string[], optional | Item ids it is known to go well with |
| `notes` | string, optional | Fit, condition, brand, care |
| `added` | string | ISO date `YYYY-MM-DD` |

Wear counts are derived from `outfits` on the page; do not store them on items.

## `outfits` — one document per time an outfit was worn (or planned)

Doc id: `YYYY-MM-DD-<event>` (add `-2` if needed).

| Field | Type | Notes |
|---|---|---|
| `date` | string | `YYYY-MM-DD` |
| `event` | string | Use the same tags as `occasions`; free text allowed for specifics ("Cousin's wedding") |
| `item_ids` | string[] | Ids from `items`. Log unknown pieces as items first |
| `colors` | string[] | Hex list, used only when pieces aren't in `items` |
| `description` | string, optional | One line if item_ids is empty |
| `rating` | number 1–5, optional | How the user felt in it |
| `status` | string | `worn` (default) or `planned` |
| `notes` | string, optional | Compliments, weather, what to change |

## `combos` — rated color pairings

Doc id: color names joined, e.g. `navy-camel` or `olive-white-brown`.

| Field | Type | Notes |
|---|---|---|
| `names` | string[] | Color names in order: ["Navy", "Camel"] |
| `colors` | string[] | Matching hex values |
| `verdict` | string | `works` or `avoid` |
| `rating` | number 1–5, optional | |
| `occasions` | string[], optional | Where it worked |
| `notes` | string, optional | |

## `outfit_ideas` — outfits suggested but not (yet) worn

Written by suggest-outfit. The page shows the newest 5 by `created`.

Doc id: `YYYY-MM-DD-<slug of name>` (add `-2` if needed).

| Field | Type | Notes |
|---|---|---|
| `name` | string | Short option name: "Tonal navy" |
| `event` | string | Occasion tag or specific event |
| `item_ids` | string[] | Ids from `items` (only owned pieces) |
| `why` | string | One line on why it works |
| `created` | string | ISO date-time, e.g. `2026-03-14T08:30:00` |
| `status` | string | `idea` (default) or `picked` once the user chooses it |
| `wada_no` | string, optional | Number of a matching combination in Sanzo Wada's *A Dictionary of Color Combinations*, only when you are confident of it |
| `wada_colors` | string[], optional | That combination's color names |

## `suggestions` — ranked things to buy next

Written by shopping-gaps. The page hides docs with `status: "bought"` and sorts the rest by `priority`.

Doc id: kebab-case slug, e.g. `light-blue-oxford-shirt`.

| Field | Type | Notes |
|---|---|---|
| `name` | string | "Light blue oxford shirt" |
| `subtype` | string | As in `items` |
| `color_name` | string | Canonical color name |
| `hex` | string | `#RRGGBB` |
| `fabric` | string, optional | |
| `reason` | string | One line on why |
| `unlocks` | string, optional | Short tag: "+6 outfits" or "covers the sangeet" |
| `priority` | number | 1 = buy first |
| `status` | string | `open` (default) or `bought` |

## `events` — multi-function events with their own shareable page

Doc id: kebab-case slug, e.g. `cousin-wedding-2026`. Created by the plan-event skill.

| Field | Type | Notes |
|---|---|---|
| `name` | string | "Cousin's wedding" |
| `url` | string | The event page artifact URL; the detailed plan lives in that page's own database |
| `start_date` / `end_date` | string | `YYYY-MM-DD` |
| `location` | string | City, country |

## `profile` — one document, `profile/me`

Captured from the user (see `page-setup.md`). Every field is optional; ask only for what a skill needs.

| Field | Type | Notes |
|---|---|---|
| `home_city` | string | Default location for forecasts |
| `country` | string | For shopping availability and shipping |
| `timezone` | string | IANA name, e.g. `America/Chicago`; resolves "today" and "yesterday" |
| `dress_style` | string | `menswear`, `womenswear` or `both`; steers foundations and traditional-wear advice |
| `undertone` | string | `warm`, `cool`, `neutral` or unknown |
| `colouring` | string | Free text the user gave: hair, eye and skin colouring |
| `flattering_colors` | string[] | Color names the user says suit them |
| `colors_to_avoid` | string[] | Color names the user dislikes or finds unflattering on themselves |
| `style_notes` | string | Anything else: fit preferences, dress code at work, budget habits |

## Write rules

- Before writing, `list` the collection (or `get` the doc) so you have its `version`; pass `if_version` when updating an existing doc.
- Use `batch` when writing more than two docs at once.
- Never invent pieces the user did not mention or show. If a field is unknown, omit it rather than guessing — except `hex`, which is always estimated from the described or photographed color.

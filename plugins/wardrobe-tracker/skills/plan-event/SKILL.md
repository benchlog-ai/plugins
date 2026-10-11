---
name: plan-event
description: Plans outfits for a multi-function event such as an Indian wedding (haldi, mehendi, sangeet, ceremony, reception) or any occasion with several dress codes, and publishes a shareable event page. Use when the user says "plan my outfits for my cousin's wedding", "each wedding function has a dress code", "the sangeet theme is pastel", "the groom's side is wearing maroon", "update the wedding plan", or "make a page I can share with family".
---

# Plan a multi-function event

Each event gets its own shareable page (an artifact) showing every function with its date, dress code, color theme, the outfit the user will wear, and the family's color coordination. The page only shows what is in its own database, so the user's full wardrobe is never exposed to family.

Two stores are involved:
- **Wardrobe** (source of pieces): the user's private Wardrobe page — see `references/data-model.md`.
- **Event page** (one per event): its own artifact database, schema below. Its URL is recorded in the wardrobe's `events` collection.

Use `ArtifactData` for both (load via ToolSearch `select:ArtifactData` if deferred). Color names, pairing rules and the user's colouring preferences: `references/color-guide.md`. Indian wedding dress-code guidance: `references/indian-wedding.md`.

**First:** find or create the Wardrobe page by following `${CLAUDE_PLUGIN_ROOT}/references/page-setup.md`, and `get` `profile/me` (for `dress_style`, colouring and home city).

## Workflow

### 1. Find or create the event
- `list` the wardrobe's `events` collection. If the event exists, use its `url` and skip to step 3.
- Otherwise gather the brief. Ask at most one AskUserQuestion round for what is missing: the functions and their dates, dress code or theme per function, location/city, and any family color plans. Unknown items can stay "TBD"; don't block on them.

### 2. Publish the event page (new events only)
1. Copy `${CLAUDE_PLUGIN_ROOT}/skills/plan-event/assets/event-page.html` to your scratchpad (or working) directory as `<event-slug>.html`, and replace `{{EVENT_TITLE}}` with a short name such as `Cousin's Wedding Outfits` (2–4 words, no dash or colon). Never use the title `Wardrobe` for an event page.
2. Publish with the Artifact tool: that file, `icon: "calendar"`, `capabilities: {"db": {}, "user": {}}`, and a one-sentence `description`.
3. Record it in the wardrobe: `set` `events/<event-slug>` with `{name, url, start_date, end_date, location}`.

### 3. Write the plan into the event page's database
- `event/info` (collection `event`, doc `info`):
  `{name, kind, host, location, start_date, end_date, notes, family_themes: [{who, names[], colors[], note}]}`
  `kind` e.g. "Indian wedding"; `who` e.g. "Groom's family", "Bride's family", "Cousins", "Me" (or the label the user prefers for themselves).
- `functions/<slug>` one per function:
  `{order, name, date (YYYY-MM-DD), time, venue, dress_code, theme_names[], theme_colors[], avoid_names[], avoid_colors[], coordination_note, outfit: {title, note, pieces: [{name, hex, category, status}]}}`
  `status` is one of `owned`, `to_buy`, `to_tailor`, `borrow`.
- Use `batch` for the initial write. Read before updating and pass `if_version`.
- Put on the event page only what the user wants family to see: no contact details, and nothing from the rest of the wardrobe.

### 4. Assign outfits
For each function, `list` wardrobe `items`, `outfits` and `combos`, then pick an outfit:
- Match the dress code and the function's formality (see `indian-wedding.md`, using the menswear or womenswear table per the profile's `dress_style`), the theme colors, and the season/weather at the event location (search the forecast if the date is within ~10 days, otherwise typical climate for that month and city).
- **Family coordination**: stay inside the function's theme; never use `avoid_colors`; do not match the colors reserved for the bride, groom or their immediate family unless the user says they are meant to; avoid wearing all-white or all-black to celebratory functions unless the theme asks for it.
- **No repeats across functions**: each statement piece (kurta, sherwani, bandhgala, Nehru jacket, saree, lehenga, anarkali) appears at most once in the event; footwear and accessories may repeat.
- Respect the user's `combos` (`avoid` never, `works` preferred) and, within the theme, favor their `flattering_colors`.
- Pieces they don't own get `status: to_buy`, `to_tailor` or `borrow`, with a concrete description (e.g. "Ivory chikankari kurta, cotton"). Do not invent owned pieces.
- Present the plan in chat as a compact table (function · dress code · outfit · gaps), then write it to the event page. Also log each function's outfit to the wardrobe `outfits` collection with `status: "planned"`, `event: "<event name> – <function>"`, and the owned `item_ids`.

### 5. Updates
When the user shares new info ("the sangeet theme changed to pastels", "the groom's side is in maroon"), update `event/info` or the function doc, re-check affected outfits for clashes, and say what changed. After the event, offer to flip the planned outfits to `worn`.

## Sharing
The page is private until the user shares it from the page's Share menu; you cannot change sharing yourself. Family members must sign in to claude.ai to see the plan. Mention this once when first publishing.

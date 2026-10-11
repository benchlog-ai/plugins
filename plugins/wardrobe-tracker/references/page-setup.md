# Find or create the Wardrobe page

Every wardrobe skill works against one private page that belongs to the user. Its exact title is **`Wardrobe`**. The page's shared database holds the whole wardrobe record (see the skill's `references/data-model.md`). Run this once per conversation before the first read or write, then reuse the URL.

Tools: the `Artifact` tool (list, publish) and the `ArtifactData` tool (database reads and writes; load it with ToolSearch `select:ArtifactData` if it is deferred).

## 1. Find

1. If the user gave the Wardrobe page URL in this conversation, use it.
2. Otherwise call `Artifact` with `action: "list"`, `scope: "mine"`, `limit: 200` and look for a row whose title is exactly `Wardrobe`.
   - One match: use its URL.
   - Several matches: use the most recently updated one and mention in one line that there are duplicates.
   - Event pages made by plan-event have other titles; never use one of them as the Wardrobe page.
3. If none is found, go to step 2 (Create). If the listing fails, ask the user once for the page link before creating a new page, so they don't end up with two.

## 2. Create (first run only)

1. Copy the template `${CLAUDE_PLUGIN_ROOT}/assets/page.html` unchanged into your scratchpad (or working) directory as `wardrobe.html`, using your file tools.
2. Publish it with the `Artifact` tool:
   - `file_path`: that copy
   - `title`: `Wardrobe`
   - `icon`: `shirt`
   - `capabilities`: `{"db": {}, "user": {}}`
   - `description`: `A live record of my wardrobe: pieces, outfits, color pairings and what to buy next.`
3. Check it once: `ArtifactData` `list` on `items`, `outfits`, `combos`, `outfit_ideas` and `suggestions` should each return an empty collection without an error.
4. Tell the user once: the link, that the page is private to them, and that it fills in as they log pieces. Do not add seed or example data.

## 3. Profile

Some defaults depend on where the user lives and what suits them. These live in the page database as one document, `profile/me` (fields in the skill's `references/data-model.md`). Never assume a city, country, timezone or colouring.

- Right after creating the page, ask one short, skippable question round: home city and country (for weather and shopping), timezone, and optionally their colouring (skin undertone, hair and eye color), colors they love or avoid wearing, and whether they mostly dress in menswear, womenswear or both. Save what they answer with `set` on `profile/me`; skip any field they don't give.
- On later runs, `get` `profile/me` when a skill needs one of these values. If a needed value is missing, ask for that one value only when it matters (for example, the city before a forecast check), then save it with `update`.
- Fallbacks when the user doesn't say: dates use the current date in the conversation's local time; weather uses the location named in the request, or is skipped with a one-line note.

## If the page can't be reached

If `Artifact` or `ArtifactData` is unavailable or returns an access error, say the Wardrobe page could not be reached, show what you would have written as a short list, and offer to retry.

# Find or create the Gourmet Trails page

Every Gourmet Trails skill reads and writes one private page that belongs to the user. Run this
once per conversation, before the first read or write, and call the result **PAGE** (its
`claude.ai` artifact link). Later steps that say "the page" or `url` = page URL mean PAGE.

The page's exact title is **`Gourmet Trails`**. Never change it; it is how the page is found.

## 1. Find

1. If the user gave a Gourmet Trails page link in this conversation, or PAGE is already known
   from an earlier step, use it.
2. Otherwise call `Artifact` with `action: "list"`, `scope: "mine"`, `limit: 200`, and look for
   an artifact whose title is exactly `Gourmet Trails`.
   - One match: that is PAGE.
   - Several matches: use the most recently updated one, and tell the user in one line that
     there are several pages with that title and which one you used.
   - No match: go to step 2 (Create). If the user says they already have a page (for example
     one shared with them from another organization), ask for the link instead of creating a
     second one.

## 2. Create (first run only)

1. Copy the bundled template into your scratchpad directory (or the working directory if there
   is no scratchpad), so the publish reads a local file:
   ```bash
   cp "${CLAUDE_PLUGIN_ROOT}/assets/page.html" "<scratchpad>/gourmet-trails.html"
   ```
   Do not edit the template. It renders an empty state and fills itself from the page's
   database and asset store.
2. Publish it as a new private artifact with `Artifact`:
   - `file_path`: the copied `gourmet-trails.html`
   - `title`: `Gourmet Trails`
   - `icon`: `restaurant`
   - `description`: `A private restaurant log with dish photos, a wishlist, Best of lists and a flavour passport.`
   - `capabilities`: `{"db": {}, "assets": {}, "downloads": {}, "user": {}}`

   `db` holds the records (`places`, `lists`, `meta/profile`), `assets` holds the dish photos,
   `downloads` lets the page's Share button save a card image, and `user` lets the page know
   whether the viewer can edit (rating dots, "+ Photo", "Been here").
3. The result's URL is PAGE. Check it once: `ArtifactData` `list`, collection `places`,
   `url` = PAGE. An empty list is the expected answer for a new page.
4. Tell the user once, in one line: the link, and that the page is private to them (only
   people they share it with from the page's Share menu can open it).

Load `ArtifactData` with ToolSearch (`select:ArtifactData`) if it is not loaded yet.

## 3. Carry on

Return to the skill that sent you here and continue with PAGE. Don't republish the page to
change data: all records go through `ArtifactData`, and photos go to the asset store
(`Artifact` with `url` = PAGE and `asset: true`). The page updates live.

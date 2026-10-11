# Find or create the Footprints page

Every Footprints skill runs this first. It gives you the page URL that every `ArtifactData` call needs.

The page title is exactly **`Footprints`**. Never use a different title.

## 1. Find

1. If the user gave a Footprints page URL earlier in this conversation, or you already found or created it in this conversation, use that URL. Stop here.
2. Otherwise list the user's artifacts: `Artifact` with `action: "list"`, `scope: "mine"`, `limit: 200`. Look for an artifact whose title is exactly `Footprints`.
   - One match: use its URL.
   - Several matches: use the most recently updated one, and tell the user in one line which one you picked (so they can point you to another).
   - No match: go to step 2, Create.
3. If the listing fails, ask the user for the page link instead of creating a second page.

## 2. Create (first run only)

Only when no page titled `Footprints` exists.

1. The page template is `${CLAUDE_PLUGIN_ROOT}/assets/page.html`. It contains no personal data: an empty map, an empty bucket list and an empty plan tab, filled from the page's database. The middle of the file is world-map geometry; read the whole file before publishing it (Read it in chunks with `offset`/`limit`).
2. Publish it as a new private artifact with the `Artifact` tool:
   - `file_path`: the template path above. If the tool refuses a path outside the working directory, Write an identical copy into your scratchpad directory and publish that copy instead. Do not change its contents.
   - `icon`: `"map"`
   - `description`: `"Your travel atlas: places visited, bucket list and trip plans."`
   - `capabilities` exactly:

     ```json
     {
       "db": {
         "rules": [
           { "path": "", "read": "view", "write": "admin" },
           { "path": "notes", "read": "admin", "write": "admin" },
           { "path": "trips", "read": "admin", "write": "admin" },
           { "path": "profile", "read": "admin", "write": "admin" }
         ]
       },
       "user": {}
     }
     ```

     These rules are what keep private memories, plans and the travel profile hidden when the user shares the page. Do not loosen them.
3. Check it once: `ArtifactData` `list` on `places` with the new URL. It should come back empty.
4. Tell the user once, in one or two lines: the link, that the page is private to them until they choose to share it from the page's Share menu, and that shared viewers only ever see the map, captions and bucket list.
5. Do not write sample data. Never write `example: true`.

## 3. Continue

Carry on with the skill, passing this URL to every `ArtifactData` call (load `ArtifactData` with ToolSearch `select:ArtifactData` if it is deferred).

If the user later says the page moved or they made a new one, use the URL they give.

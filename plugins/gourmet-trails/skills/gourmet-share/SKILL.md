---
name: gourmet-share
description: Makes shareable Gourmet Trails content — a recommendation card image (PNG for WhatsApp or Instagram) for one restaurant, "Best of" lists that collect favourite places on the page, and a one-image Best of list card to send to friends. Use when the user says "make a share card for Saffron House", "send me an image of Hoshi Izakaya for Instagram", "a story-size card", "make a Best of brunch list", "add Cedar & Sumac to my Lebanese list", "what's in my Best of lists?", "send my brunch list to Maya", or "share my Best of Italian".
---

# Share cards and Best of lists

**Page first:** follow `${CLAUDE_PLUGIN_ROOT}/references/page-setup.md` to find or create the
user's Gourmet Trails page (PAGE). Data model:
`${CLAUDE_PLUGIN_ROOT}/skills/gourmet-log/references/data-model.md`.

The cards are signed with the `name` from `meta/profile` ("Maya recommends"). Read it once
(`ArtifactData` `get`, collection `meta`, doc `profile`). If it is not set, leave `--by` out
and the card says "Recommended"; don't ask for a name just for this.

## Share card (PNG)

1. `ArtifactData` `get` the place. If it has no photos, ask the user for one (a card without a
   photo isn't worth sending). If `needsName` is true, ask for the name first.
2. Download the cover photo: `Artifact` `action: "read"`, `url` = PAGE, `path` = the photo's
   asset id. Use the saved file path from the result.
3. Render:
   ```bash
   pip install --break-system-packages -q pillow 2>/dev/null
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/gourmet-share/scripts/make_card.py \
     --photo <cover.jpg> --name "<name>" --cuisine "<cuisine>" --area "<area>" \
     --city "<city>" --order "<order>" --note "<note>" --rating <0-5> \
     --by "<profile name>" --size post --out gourmet-<slug>.png
   ```
   `--size story` gives 1080×1920 for stories. Omit `--note` when the place has none; never
   invent one. `--rating 0` hides the dots. Omit `--by` when the profile has no name.
   `--footer` changes the brand line at the bottom (default "GOURMET TRAILS").
4. Look at the PNG once (Read it). Check the name fits and nothing overlaps.
5. Send it with `SendUserFile` (`display: "render"`) and a one-line caption; if that tool is
   not available, give the file path. Offer the copy text for WhatsApp in the reply when
   useful.

The page also has a Share button that saves the same card from the browser; this skill is for
cards made from chat or in story size.

## Best of lists

Lists live in the `lists` collection and appear on the page's "Best of" tab.

- **Create**: pick places from `places` that match the user's request (by cuisine, rating,
  area or occasion), order them best first, and propose the list in one message before writing
  (title, 3–6 places, a one-line note). Write it on their OK.
- **Edit**: add, remove or reorder `placeIds`; update `title`/`note`. Pin writes with
  `if_version`.
- **Share with friends**: a Best of list goes out as one image, not as access to the page.
  1. Download each place's cover photo (`Artifact` `action: "read"`, `url` = PAGE,
     `path` = asset id) into one folder.
  2. Write `list.json` in that folder: `title`, `note`, `by` (the profile `name`; leave it out
     if unset), optionally `footer`, and per place `name`, `area`, `city`, `order`, `rating`,
     `photo` (file name). Use only fields the records have.
  3. Render and check it once:
     ```bash
     python3 ${CLAUDE_PLUGIN_ROOT}/skills/gourmet-share/scripts/make_list_card.py \
       --spec <folder>/list.json --out best-of-<slug>.png [--size story]
     ```
  4. Send it with `SendUserFile` (`display: "render"`, or the file path if that tool is not
     available) plus a paste-ready text version for WhatsApp: the title, then one line per
     place ("1. Morning Table, Old Town: order the shakshuka"), and the Maps links on request.
  The page itself stays private (it holds the wishlist and every visit). If the user wants a
  friend to browse it, they share it from the page's Share menu; say so once, only when they
  ask.
- **Friends' picks back in**: when a friend replies with their own places, that is
  `gourmet-friends`.

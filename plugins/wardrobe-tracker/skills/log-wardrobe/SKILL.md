---
name: log-wardrobe
description: Records wardrobe pieces, accessories, outfits worn and color pairings into the user's Wardrobe page. Use when the user says things like "add my navy blazer", "log this shirt" (with or without a photo), "I wore X to the office today", "log today's outfit", "navy and camel works for me", "never pairing olive with brown again", or "remove/update an item".
---

# Log to the wardrobe

Keep the user's wardrobe record current. The record is the shared database of their private **Wardrobe** page, read and written with the `ArtifactData` tool (load via ToolSearch `select:ArtifactData` if deferred). The page updates live after every write.

**First:** find or create the Wardrobe page by following `${CLAUDE_PLUGIN_ROOT}/references/page-setup.md`.

Read `references/data-model.md` before the first write in a session, and `references/color-guide.md` whenever assigning a color name or hex.

## Workflow

1. **Work out what is being logged**: a new piece/accessory (`items`), an outfit worn or planned (`outfits`), a color pairing verdict (`combos`), or an edit/removal.
2. **Load current state**: `list` the relevant collection(s) so duplicates are caught and versions are known. For outfits, also `list` `items` to resolve piece names to ids.
3. **Extract fields**
   - From text: take what the user said; fill category, subtype, formality, seasons and occasions from common sense for that garment (a wool blazer is formality 4, autumn/winter, office/formal). Do not invent brand, fabric or fit.
   - From a photo: Read the image, identify each visible piece, its dominant color (and a secondary color if patterned), pattern and likely fabric. If the photo shows a full outfit, log the pieces that are not yet in `items`, then log the outfit.
   - Colors: map to the canonical names in `color-guide.md`; estimate hex from the photo when one is provided.
4. **Match existing items**: if a piece plausibly matches an existing item (same subtype and color), reuse its id instead of creating a duplicate; when unsure between two, ask with one short question.
5. **Write**: one `set` for a single doc, `batch` for several. Use `update` with `if_version` for edits. Delete only when the user asks.
6. **Confirm briefly**: one or two lines naming what was saved (e.g. "Added Navy wool blazer (outerwear, office/formal) and logged today's office outfit with 3 pieces."). Mention a notable pairing observation only if it is useful. Do not paste the page URL unless asked or the page was just created.

## Defaults

- Outfit date defaults to today in the user's `timezone` from `profile/me`; if none is saved, use the current local date of the conversation. "Yesterday" etc. resolve relative to that.
- Outfit `status` is `worn` unless the user says they are planning it.
- When the user rates or reacts to an outfit ("felt great", "too formal"), capture it in `rating`/`notes`.
- When the user states a pairing works or doesn't, write a `combos` doc as well as any outfit.
- When the user picks or wears an outfit that is in `outfit_ideas`, set that idea's `status` to `picked`.
- When the user says they bought a piece that is in `suggestions`, log it to `items` and set the suggestion's `status` to `bought`.
- If the user mentions their colouring, colors that suit them, colors they avoid wearing, their city or timezone, save it to `profile/me` with `update`.

## If the database is unreachable

If `ArtifactData` is unavailable or returns an access error, tell the user the Wardrobe page could not be reached, show the record you would have written as a short list, and offer to retry.

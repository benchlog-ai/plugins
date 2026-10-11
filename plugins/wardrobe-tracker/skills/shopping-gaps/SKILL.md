---
name: shopping-gaps
description: Identifies which pieces or accessories the user should buy next to unlock the most new outfits or cover an upcoming event, based on their recorded wardrobe. Use when the user asks "what should I buy next", "what's missing from my wardrobe", "I have a budget for one new piece", "do I need anything for the wedding in December", or "shopping list for winter".
---

# Shopping gaps

Work from the database of the user's private **Wardrobe** page via `ArtifactData` (load via ToolSearch `select:ArtifactData` if deferred). Fields are in `references/data-model.md`; pairing principles and the user's colouring preferences in `references/color-guide.md`.

**First:** find or create the Wardrobe page by following `${CLAUDE_PLUGIN_ROOT}/references/page-setup.md`.

## Workflow

1. `list` `items`, `outfits`, `combos`, `suggestions` and `events`; `get` `profile/me`.
2. Note the context the user gives: season, upcoming events, budget, a piece count limit, style direction.
3. **Find gaps**:
   - Missing foundations, adapted to the profile's `dress_style` (ask once if unknown and it matters). Menswear: a white and a light-blue shirt, navy and grey trousers, dark denim, a navy or charcoal blazer, brown and black leather shoes with matching belts, a versatile watch, a weather-appropriate coat. Womenswear: a white shirt or blouse, a fine-knit top, tailored trousers in navy or black, dark denim, a versatile skirt or dress, a blazer, neutral flats and a heeled or dressy shoe, a structured bag, a weather-appropriate coat.
   - Occasion gaps: occasions with fewer than 3 complete outfits at the right formality (include any event the user mentions or that is in `events`).
   - Season gaps: few pieces for the coming season.
   - Orphans: pieces that pair with almost nothing the user owns; a single bridging item can rescue them.
4. **Score candidates** by how many new valid outfits each would unlock with existing pieces (respecting formality, season, `avoid` combos and the profile's `colors_to_avoid`). Count roughly; show the reasoning in a phrase, not a calculation dump.
5. **Recommend** a ranked list of 3–5 purchases: the piece (category, color name, fabric), why, and roughly how many new outfits it unlocks or which event it covers. Respect any budget or count limit. If the user asks for product links or prices, search the web for current options available in the profile's `country` (or that ship there); if no country is saved, ask once.
6. **Show it on the page**: replace the open list in `suggestions` with the new ranking in one `batch` — `set` each recommended piece (`name`, `subtype`, `color_name`, `hex`, `fabric`, `reason`, `unlocks`, `priority`, `status: "open"`) and `delete` any older `open` suggestion that is no longer recommended. Leave `bought` docs alone.
7. Offer to add any piece the user buys to the wardrobe (follow log-wardrobe conventions) and mark its suggestion `bought`.

Do not write to `items` unless the user confirms a purchase.

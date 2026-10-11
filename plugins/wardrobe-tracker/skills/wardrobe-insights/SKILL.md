---
name: wardrobe-insights
description: Analyses the user's wardrobe record for color balance, wear patterns, rarely worn pieces, favorite combinations and occasion coverage. Use when the user asks "what do I wear most", "which pieces am I ignoring", "how balanced are my colors", "give me a wardrobe review", "what are my go-to combos", or "monthly style recap".
---

# Wardrobe insights

Analyse the database of the user's private **Wardrobe** page with `ArtifactData` (load via ToolSearch `select:ArtifactData` if deferred). See `references/data-model.md` for fields.

**First:** find the Wardrobe page by following `${CLAUDE_PLUGIN_ROOT}/references/page-setup.md`. If it has to be created, the wardrobe is empty: say so and offer to log pieces instead of running an analysis.

## Workflow

1. `list` `items`, `outfits` and `combos` (page with `query.cursor` if `next_cursor` is returned).
2. Compute, counting only outfits with `status` `worn` (or no status):
   - **Color balance**: share of pieces by color name; neutrals vs accents; missing neutral anchors (no white shirt, no navy, no brown shoes, etc.).
   - **Wear frequency**: times worn and last worn per item; top 5 most worn; pieces never worn or not worn in 60+ days.
   - **Combinations**: most frequent color sets and piece pairs across outfits; highest-rated outfits; `works`/`avoid` pairings from `combos`.
   - **Occasion coverage**: for each occasion tag, how many complete outfits (top + bottom + footwear, or a dress/suit/traditional set + footwear, at a matching formality) are possible. Flag occasions with fewer than 3.
   - **Accessories**: which accessories are used and which never appear in outfits.
3. Report concisely: a short headline summary (2–3 sentences), then sections for the points that are actually notable. Use small tables only where they help. Close with 2–3 concrete actions (e.g. "Wear the burgundy knit with grey trousers this week", "Retire or donate the beige polo — not worn in 4 months").
4. If the user asks for a timeframe ("this month"), filter outfits by `date`.

Keep claims grounded in the data; if there are fewer than ~10 outfits logged, say patterns are early and keep conclusions tentative. Do not write to the database during an insights run.

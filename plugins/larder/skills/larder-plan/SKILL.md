---
name: larder-plan
description: Plans balanced meals in the user's Larder week calendar and suggests recipes. Use when the user says "plan my week", "what should I cook tonight", "suggest dinner with what I have", "something seasonal", "a cuisine I haven't tried", "what's trending", "plan Friday lunch", "I cooked dinner", or "mark tonight's dinner as cooked".
---

# Larder meal plan

Meals live in the `plan` collection of the user's Larder page and appear in its Week tab as expandable day rows. Each meal carries a description, ingredients and method, so the user can read the dish without opening anything else.

Read `references/schema.md` first for the meal document shape and the matching rules.

## Suggesting and planning

1. **Locate the page.** Follow `${CLAUDE_PLUGIN_ROOT}/references/page-setup.md` to find the user's page titled "Larder", or create it on first run. Its kitchen profile step makes sure region, diet and servings come from the user.
2. **Gather context.** Read `settings/kitchen` (region, diet and dislikes, servings), the `pantry` collection (what is in stock, what is use-soon) and the `plan` collection for the target week (avoid repeating dishes).
3. **Research when it helps.** For "in season", "trending" or "new cuisine" requests, use web search if it is available so the ideas are current, and say where trends come from. Use the region from settings for seasonality, and the current date. If search is not available, say that the ideas come from general knowledge.
4. **Design balanced plates.** Aim for vegetables, a protein, a carbohydrate and a source of healthy fat across each meal, and record this in `groups`. Prefer stocked ingredients, and keep new purchases short.
5. **Offer, then write.** For a single slot, propose two or three options in a few lines each and write the one the user picks. For "plan my week", propose the list of dishes first, then write them in one `batch` after approval. Do not overwrite an existing meal in a slot without asking.
6. **Write each meal** with `set` at the id `YYYY-MM-DD-slot` (slot is `lunch` or `dinner`): title, cuisine, minutes, description, one-line `why`, `groups`, `ingredients` (with `name`, `qty`, `unit`), 4 to 6 short `steps`, `status: "planned"`. In ingredients, use the exact pantry item name when the item is stocked, so the page can match it.
7. **Tell the user what is missing.** After planning, compare ingredients with the pantry and mention what is not in stock. Offer to add those to the shopping list (see the `larder-shop` skill).

## Marking a meal cooked

When the user says they cooked a planned meal:

1. Read the meal and match each ingredient to a pantry item.
2. For each match with the same unit, subtract the recipe quantity from `qty` (never below 0). Skip ingredients whose unit differs and say which ones need a manual adjustment.
3. Apply the pantry updates and the meal update (`status: "cooked"`, `cookedAt` as an ISO timestamp) in one `batch`.
4. Report what came off the shelves in one or two sentences, and name anything that is now out or low.

If the user cooked something that was not planned, create the meal document with `status: "cooked"` for the date they cooked it, then deduct as above.

## Rules

- Respect `prefs` in settings every time. Never invent a diet, allergy or dislike.
- Use servings from settings when scaling quantities. If servings is not set, ask once (see the kitchen profile step) rather than guessing silently.
- Do not write `example: true`.
- Never delete a cooked meal. The calendar is the record of what was cooked.

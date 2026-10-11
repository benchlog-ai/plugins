---
name: larder-shop
description: Builds and manages the user's Larder shopping list. Use when the user says "make my grocery list", "what do I need for this week", "add lemons to the list", "add what's running low", "I bought the chicken", "I'm back from the shop", "clear the list", or "what's left to buy".
---

# Larder shopping list

The list lives in the `shop` collection of the user's Larder page. The user ticks items off in the page while shopping, and each tick puts the item on the pantry shelves automatically. Keep that behaviour identical when you do the same thing from chat.

Read `references/schema.md` first for the list item shape and the stocking rules. Before the first read, follow `${CLAUDE_PLUGIN_ROOT}/references/page-setup.md` to find the user's page titled "Larder", or create it on first run.

## Building the list

1. Read `pantry`, `plan` and `shop`.
2. **From the plan:** for every planned meal that is not cooked, compare each ingredient with the pantry. Missing items are needed in full. Items with the same unit and too little stock are needed for the difference. Add up shortfalls across meals so one item appears once.
3. **From low stock:** add items that are low (qty 0, or qty / par at most 0.25). Request the amount that brings them back to `par`, or 1 when `par` is empty.
4. Skip anything already on the list and unticked.
5. Write with `batch`: `name`, `qty`, `unit`, `area`, `zone` (copy these from the matching pantry item when there is one), `checked: false`, `source` (`plan`, `low`, `manual` or `claude`) and `for` (the meal titles, shortened). Leave `example` out.
6. Summarise by section in the order a shop is walked (produce, protein, pantry) in a few lines.

## Marking items bought

Treat "I bought X" like a tick in the page, so the shelves and the list agree:

1. Find the shop item. Find a pantry item with the same normalized name and unit.
2. If found, add the bought quantity to its `qty`. If not, create a pantry item (see the schema for kind, colour, unit and zone guidance) with `par` equal to the quantity.
3. Update the shop item: `checked: true`, `pantryId` (the pantry document id), `added` (the quantity), `created` (true when you made the pantry item).
4. For a whole shop, do all of it in one `batch`.

To undo a tick, subtract `added` from the pantry item (delete it if `created` is true and nothing else was added), then clear `checked`, `pantryId` and `added`.

## Clearing

- "Clear the ticked ones" deletes only items with `checked: true`. Their stock is already on the shelves.
- "Clear the list" deletes everything. Confirm first when unticked items remain.

## Rules

- Do not write `example: true`.
- Keep names plain and singular-friendly ("Chicken thighs", "Bok choy") so they match pantry items.
- Never add the same item twice. Raise the quantity of the existing line when more is needed.

---
name: larder-pantry
description: Keeps the user's Larder pantry current. Use when the user says things like "add milk to the fridge", "I used the last of the cumin", "I cooked the curry, update the shelves", "throw out the spinach", "what's running low", "what's in my pantry", "stock my kitchen from this photo or list", or "what should I use up soon".
---

# Larder pantry

The pantry lives in the user's Larder page, a shared database that the user sees as drawn shelves (pantry cupboard, produce crisper, protein fridge). Every change you write appears there live.

Read `references/schema.md` before the first read or write in a conversation. It holds the collections, field meanings and the matching rules.

## Workflow

1. **Locate the page.** Follow `${CLAUDE_PLUGIN_ROOT}/references/page-setup.md` to find the user's page titled "Larder", or create it on first run.
2. **Read before writing.** `ArtifactData` `list` or `query` the `pantry` collection. Match what the user names against existing items by name (singular/plural and extra words such as "tinned" do not matter). Never create a duplicate of something already on a shelf.
3. **Write the change.**
   - Adjusting stock: `update` the item's `qty`, pinned with `if_version`. Round to 2 decimals. Quantity never goes below 0.
   - Used up: set `qty` to 0. The page shows a faded "OUT" shape, which keeps the slot visible for restocking.
   - Thrown away or no longer kept: `delete` the document.
   - New item: `set` a new document with every field in the schema. Pick `area`, `zone`, `kind`, `color` and `unit` with the guidance in the schema, set `par` to the quantity bought, and leave `example` out.
   - Several changes at once (after cooking, a restock from a receipt, a photo or a list): one `batch`.
4. **Report briefly.** Say what changed in one or two sentences, for example "Took 150 g red lentils and 200 g spinach off the shelves, spinach is now out."

## After a cooked meal

When the user says they cooked something that is in the `plan` collection, follow the cooking steps in the `larder-plan` skill so the meal is marked cooked and the stock is deducted in one pass. When it is not in the plan, deduct the quantities the user gives, or the recipe quantities you would normally use, and tell them which numbers you assumed.

## Running low and use-soon

An item is low when `qty` is 0, or `par` is set and `qty / par` is 0.25 or less. An item is use-soon when `expires` is within 3 days of today and `qty` is above 0. List these when asked, and offer to add the low ones to the shopping list (see the `larder-shop` skill).

## Rules

- Do not write `example: true`. Items marked as samples are placeholders the user may clear.
- Do not delete items to tidy up. Delete only when the user says something is gone or asks for removal.
- Quantities stay in the item's existing unit. If the user gives another unit, convert only when it is obvious (kg to g, l to ml); otherwise ask.
- Photos of a fridge or receipts: list what you read, then write only after the user confirms uncertain items.

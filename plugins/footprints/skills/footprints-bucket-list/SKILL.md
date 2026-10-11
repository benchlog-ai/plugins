---
name: footprints-bucket-list
description: Manages the user's Footprints bucket list of places they want to visit, shown as illustrated postcards. Use when the user says "add Patagonia to my bucket list", "I want to see the northern lights someday", "move Tromsø to next up", "what's on my bucket list", "remove Bali", or "which bucket list places fit March".
---

# Bucket list

First get the page URL with `${CLAUDE_PLUGIN_ROOT}/references/page-setup.md` (find the page titled "Footprints", or create it on first run). Then read `references/schema.md`.

## Adding

1. Read `bucket` and `places`. If the place is already on the list, update it instead. If the user has already been there (in `places`), say so and ask whether it's a return trip they want listed.
2. Fill the card from what they said plus well-established facts about the place:
   - `why`: their reason in their words. If they gave none, write one plain sentence on what the place is known for and say so, so they can change it.
   - `season`: the commonly recommended months for what they want to do there (aurora, hiking, festivals). Search the web if you aren't sure.
   - `scene`: the postcard illustration that matches the place's signature landscape.
   - `priority`: 3 unless they say otherwise.
   - `lat`/`lng`: approximate centre.
3. `set` the document. Several at once go in one `batch`.
4. Reply in one line ("Added Tromsø as a winter someday trip, best Feb–Mar for aurora").

## Answering questions

- "What's on my list?": group by priority, one line each with best season.
- "What fits <month>?": filter by `season`, then rank using `profile/travel` (pace, budget, flight limits from the home airport in `profile/travel.home`). If no home is saved, ask once as `references/schema.md` describes, or rank without flight limits if they'd rather not say. Say why each fits in a phrase.

## Changing and removing

- Priority or details: `update` with `if_version`.
- Remove: `delete` the doc (and its `photos/{photoId}` if set). If a trip in `trips` has this `bucketId`, leave the trip alone.

## Moving to a plan

"Let's plan Tromsø" → hand over to the `footprints-plan-trip` skill with this card as the starting point and set the trip's `bucketId`.

## Rules

- The bucket list is visible on shared links. Keep budgets, companions and dates out of it.
- Don't write image URLs. The page draws the postcard; the user can upload their own photo on the page.

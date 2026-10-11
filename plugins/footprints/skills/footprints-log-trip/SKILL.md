---
name: footprints-log-trip
description: Adds or updates a visited place on the user's Footprints map with dates, a shareable caption, highlights and private memories. Use when the user says "I just got back from Porto", "log my trip to Kyoto in April 2023", "add Edinburgh to my map", "add a memory to Lisbon", "fix the dates on my Iceland pin", "remove the Prague pin", or "mark the Marrakech trip as done".
---

# Log a trip

First get the page URL with `${CLAUDE_PLUGIN_ROOT}/references/page-setup.md` (find the page titled "Footprints", or create it on first run). Then read `references/schema.md`.

## Steps

1. **Read** `places` (and `notes` if editing). Match by name and year. If the same place exists from a different year, this is a new pin unless the user says it's the same trip.
2. **Gather** what's missing, in one short message at most: dates (month is enough), one line they'd show friends, a highlight or two. Don't interrogate. If they gave a quick "log Porto May 2024", write it straight away and offer to add memories after.
3. **Write** in one `batch`:
   - `places/{slug-year}` with coordinates, country, dates, caption, highlights, tags, rating (only if given).
   - `notes/{same id}` with private details: who they went with, stories, food spots, costs.
   - A trip of several stops (e.g. Rome + Florence + Venice) becomes one pin per stop with the same date range split as they describe.
4. **Report** in one or two sentences, e.g. "Pinned Porto (May 2024) with your note about the francesinha. That's 23 countries now."

## Turning a plan into a footprint

When the user says a planned trip happened ("I'm back from Marrakech", "mark the trip done"):

1. Read the trip in `trips`. Set `status: "done"`.
2. Create a pin for each `days[].base` that's a distinct place, dates from the trip.
3. Ask what actually happened: favourite moment, best meal, anything that didn't go to plan. Write the shareable part as `caption`/`highlights` and the rest to `notes`.
4. If the trip came from the bucket list (`bucketId`), ask whether to remove that bucket card. Don't remove it unasked.
5. Offer a short animated recap (see `footprints-recap`).

## Edits and removals

- Edits: `update` only the changed fields with `if_version`.
- Removal: `delete` `places/{id}` and `notes/{id}`; if the place had a `photoId`, delete `photos/{photoId}` too. Confirm first if it has a caption or memory.

## Rules

- Captions are public. Keep names of people, prices and anything private in `notes`.
- Use the user's words for memories. Tidy grammar, don't embellish.
- Never write `example: true`.

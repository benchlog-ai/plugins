---
name: footprints-onboard
description: Interviews the user like an experienced travel planner and saves their travel profile (including home city and airport) and past trips to their Footprints page. Use when the user says "interview me", "onboard me", "let's set up Footprints", "update my travel profile", "ask me about my travel style", "here are the places I've been", or pastes a list of past trips.
---

# Footprints onboarding

Two jobs, either or both in one session:

1. **Travel profile** → `profile/travel`
2. **Backfill past trips** → `places` (+ `notes`)

First get the page URL with `${CLAUDE_PLUGIN_ROOT}/references/page-setup.md` (find the page titled "Footprints", or create it on first run). Then read `references/schema.md` for the fields and privacy rules. Read `profile/travel` and list `places` before asking anything, so you never ask for what is already saved. Resume where it left off.

## How to interview

Act like a senior travel planner meeting a client: warm, curious, concrete. Ask **two or three questions per turn**, never a form. Use `AskUserQuestion` for questions with natural options (pace, budget band, trip length) and plain text for open ones. Follow up on interesting answers ("You said the best meal of your life was in Kyoto. Was it the food itself or the setting?") because the follow-ups produce the best recommendations later.

Cover these areas, in roughly this order, skipping any already filled:

1. **Home base and rhythm**: home city and country, the airport they usually fly from, how many trips a year, long weekends vs. weeks, months they can't travel. Home comes first because every other skill uses it (flight searches, arcs on the map, public holidays).
2. **Pace and style**: slow or packed, planned or spontaneous, hotels vs. guesthouses, solo or with others.
3. **What makes a trip great**: favourite trip so far and why, a disappointing one and why.
4. **Food**: what they hunt for (street food, fine dining, markets, cooking classes), anything they won't eat.
5. **Photography**: what they shoot (landscape, street, food), gear they carry, golden-hour priorities.
6. **Nature and climate**: hiking level, heat/cold tolerance, beaches vs. mountains.
7. **Budget**: typical per-trip spend, the currency they think in, and where they splurge.
8. **Practical constraints**: passport and visa situation, flight length limit, vacation days. Store under `constraints` only if they state them.
9. **Avoid list**: crowds, cruise ports, long transfers, etc.

After every two or three answers, write what you learned (`update` on `profile/travel` with `if_version`; `set` it the first time). Save `home` as `{name, country, region?, lat, lng, code}` from what the user said, with coordinates from well-known city values and the airport's IATA code; never fill it with a guess they didn't give. Saving as you go means an interrupted interview is never lost. Set `updated` to now.

When the profile has enough to recommend from (at least home, pace, interests, food and budget), say so in one line and offer to backfill past trips or stop.

## Backfilling trips

- Accept any shape: a pasted list, "Lisbon 2023, Kyoto April 2024", or one trip at a time.
- For a list, write all pins in one `batch` with coordinates, `from` (as precise as given), `country`, and empty captions. Don't stop to ask about each.
- Then offer to go through them one by one for memories. For each: ask for a highlight or two and one shareable line, then write the `caption`/`highlights` to `places` and anything personal (who with, stories, costs) to `notes`.
- If the page has example pins (`example: true` or ids starting `ex-`), mention once that "Clear examples" on the page removes them.

## Rules

- Write only what the user said. Paraphrase into tidy phrases, but don't add opinions or invent details.
- Never put anything personal in `places` or `bucket`. Those are visible when the page is shared.
- Finish with a two-line summary of what was saved and what's left.

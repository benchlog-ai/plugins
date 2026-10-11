---
name: footprints-recommend
description: Recommends where the user should travel next, based on where they have been, what they loved, their bucket list and their travel profile in Footprints. Use when the user asks "where should I go next?", "suggest a long weekend in November", "somewhere warm in February", "a food trip I haven't done", "what fits the next public holiday weekend", or "surprise me".
---

# Recommend the next trip

First get the page URL with `${CLAUDE_PLUGIN_ROOT}/references/page-setup.md` (find the page titled "Footprints", or create it on first run). Then read `references/schema.md`.

## Gather

Read `profile/travel`, `places`, `notes`, `bucket` and `trips` (one call each, in parallel). Note:

- **What they love:** tags, ratings of 4–5, captions and memories that light up (food, light, hiking). Ratings of 1–2 and "didn't love" notes are just as useful.
- **Where they've been:** countries and regions, so you don't repeat them unless a return is the point.
- **What's queued:** bucket items and their seasons; trips already planned.
- **Constraints:** home city and airport (`profile/travel.home`), trip length, budget, flight limits, months they can't travel, passport/visa notes.

If `home` is missing, ask once as `references/schema.md` describes (flights, prices and holidays all depend on it). If the rest of the profile is empty, say that recommendations get much better after a five-minute interview (`footprints-onboard`), then still give a best-effort answer from their pins.

## Recommend

1. Work out the window: dates or month they gave, else the next sensible slot. For public holidays, long weekends and bridge days, use the user's home country (and region, if saved) from `profile/travel.home`: search the current year's official list rather than relying on memory. If no country is saved, ask which country's holidays apply.
2. Shortlist 3 options, mixed on purpose:
   - one from their **bucket list** whose season matches,
   - one **"you'd love this because…"** pick that extends something they rated highly (e.g. loved Kyoto's temples and food → Kanazawa, or Luang Prabang),
   - one **wildcard** that fits their profile but nothing they've done.
3. For each, check the current facts that decide it: direct or one-stop flights from their home airport and typical price (Kiwi.com tool if loaded), weather for those dates, any visa issue given their nationality and constraints, events or closures. Search the web; don't guess.
4. Present each in 3–4 lines: where, when, why it fits them (name the pin or preference it builds on), rough cost and flight time, the trade-off. Then one line on which you'd pick and why.

Use the `comparison_card_display_v0` widget only if they ask to compare; otherwise plain prose.

## Follow-through

- "Add it to my list" → `footprints-bucket-list`.
- "Let's plan it" → `footprints-plan-trip`, carrying the reasoning into the trip `summary`.

## Rules

- Ground every "because" in something stored or said. Don't claim they like things they never said.
- Recommendations live in chat. Don't write anything to the page unless they ask (saving a missing `home` is the one exception).

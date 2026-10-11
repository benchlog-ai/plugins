---
name: footprints-plan-trip
description: Plans a trip with the user in chat, then lays out the itinerary, packing checklist and tickets to book on the Plan tab of their Footprints page. Use when the user says "plan a week in Morocco in May", "help me plan Tromsø", "let's plan the Scotland long weekend", "refine my Marrakech plan", "swap day 3", "check flights for the trip", "what do I need to pack", "lock it in", or pastes the page's "Use Footprints to refine…" prompt.
---

# Plan a trip

First get the page URL with `${CLAUDE_PLUGIN_ROOT}/references/page-setup.md` (find the page titled "Footprints", or create it on first run). Then read `references/schema.md`. Then read `profile/travel`, `places` and the relevant `trips`/`bucket` docs. The profile shapes everything: pace, budget, food, photography, constraints, and the departure airport in `home.code`. If `home` is missing, ask once as `references/schema.md` describes and save it before searching flights.

## 1. Brainstorm (chat only)

Before writing anything, work out the shape of the trip with the user, like a good planner would:

- Pin down the essentials, asking only what you can't infer: dates or month, number of days, who's going, budget, the one thing that would make the trip.
- Propose **two or three distinct shapes** (e.g. "city-heavy with a mountain day" vs. "split stay with two bases"), each in three or four lines with why it suits their profile and what it trades off. Draw on what they loved and disliked in `places`/`notes`.
- Check the practical facts that change the plan: season and weather, opening days, visa needs given their `constraints` and home country, flight routes from their home airport. Search the web for anything current; cite sources in chat.
- As soon as a direction is chosen, write the trip with `status: "brainstorm"` (or update it) with `title`, `destination`, `summary`, rough `start`/`end`. This makes it appear on the page right away.

## 2. Draft and refine

Draft the full plan in chat as a compact day-by-day outline, then iterate on the user's feedback. Keep the page in sync after each round they agree with, so they can look at it while chatting.

**Itinerary (`days`)**
- One entry per day with `date`, a short `title`, `base` (where they sleep) and 3–6 `items`.
- Respect their pace. Leave room for golden hour photography and for meals that matter; name specific places only when you've checked they exist and are open then.
- Travel days list the transport with realistic times.

**Tickets (`tickets`)**
- Everything that must be booked: flights, trains, stays, timed entries, cars, guides, insurance.
- Use the Kiwi.com tool for flights from the user's home airport (`profile/travel.home.code`; load with ToolSearch `select:mcp__Kiwi_com__search-flight`) and Booking.com for stays and attractions when useful. Put the best 1–2 real options in `detail` and the price as a number, with `currency` as quoted (the profile's `currency` when it matches). Searching is fine; **never book or pay**. The user books themselves.
- `bookBy`: when prices or availability usually force a decision (flights ~6–8 weeks out, popular timed entries per their booking window). Say how you estimated it.
- On rewrite, keep `status`, `ref` and `link` of tickets they already booked.

**Packing (`packing`)**
- Built from the destination's weather for those dates, the activities, trip length and their photography kit. Grouped: Documents, Clothes, Photo, Tech, Toiletries, Health, Other.
- Practical and specific ("Warm layer for nights in the Atlas Mountains", "UK plug adapter"). Pick plug adapters by comparing the destination with the home country. Don't pad with obvious items.
- On rewrite, keep every existing item's `done` state and any items in group "Added".

Set `status: "planning"` once days are drafted.

## 3. Lock it in

When the user says "lock it in" or similar: read the trip, merge your final version with their edits on the page (ticked items, booked tickets, added items), write once with `if_version`, and summarise in two lines (days, tickets still to book with the nearest book-by date).

When everything is booked, suggest `status: "booked"`.

## Refining later

"Swap day 3", "make it slower", "add a food tour": read the trip, change only what's asked, write back, and say what changed in one line.

## Rules

- The trip lives in `trips`, which is private. Never copy plan details into `places` or `bucket`.
- One trip per document. A multi-country journey is still one trip.
- Don't invent opening hours, prices or routes. If you couldn't verify something, mark it in the item `note` ("check hours").

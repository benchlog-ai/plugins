---
name: gourmet-onboard
description: Sets up Gourmet Trails for the user — creates their private page on first run, runs a short taste interview saved as their taste profile, and bulk-imports past restaurant visits from a batch of food photos or a list of places. Use when the user says "set up Gourmet Trails", "interview me about food", "update my taste profile", "import my food photos", "here's a folder of restaurant photos", or pastes a list of restaurants they have been to.
---

# Onboard Gourmet Trails

**Page first:** follow `${CLAUDE_PLUGIN_ROOT}/references/page-setup.md` to find or create the
user's Gourmet Trails page (PAGE). Data model:
`${CLAUDE_PLUGIN_ROOT}/skills/gourmet-log/references/data-model.md`. Photo handling:
`${CLAUDE_PLUGIN_ROOT}/skills/gourmet-log/references/photo-workflow.md`.

## Part 1: Taste interview

Read `meta/profile` first (`ArtifactData` `get`, `url` = PAGE, collection `meta`, doc
`profile`); if it exists, only ask about what is missing or what the user wants to change.

Ask like a friend who knows food, a few questions at a time (use AskUserQuestion where the
answers are choices), never a form:

1. Cuisines they love, and the one dish they would cross town for.
2. Anything they don't eat (dietary choices as they state them).
3. Spice: how much heat they like.
4. Usual budget, and what they spend on a special occasion.
5. Who they usually eat with, and the usual occasions (weekday lunch near work, weekend
   brunch, date night).
6. Home base for distance: the city and neighbourhood they eat around most (home, work).
7. A cuisine they have never tried but are curious about. This seeds the wishlist.
8. Optional: the name to show on share cards and the page header ("Maya recommends"). A first
   name or a handle; skip it if they'd rather not, and cards then say "Recommended".

Write the answers to `meta/profile` (`set` when new, `update` with `if_version` otherwise).
If the user mentions an allergy or health condition, use it in this conversation but do not
store it.

## Part 2: Import past visits

- **From the Mac Photos library** (macOS only): run the `gourmet-photos` skill over the period
  the user names ("the last two years").
- **From photos**: follow `photo-workflow.md`. Process in batches of up to 25 photos. Group by
  visit, identify restaurants from metadata and visual clues, create one place per restaurant,
  and collect every unidentified group into a single question for the user at the end
  ("Which restaurant was the tapas dinner with croquetas and pinchos?").
- **From a list of names**: web-search each to confirm city, area and cuisine; create
  `status: "visited"` places without ratings, then ask the user for ratings in one message
  ("Quick ratings 1–5: Saffron House, Hoshi Izakaya, …").

Finish with one short summary: places added, cuisines stamped, names still needed. Offer one
next step: rating the new places, or "where should we eat this week?".

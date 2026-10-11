---
name: gourmet-recommend
description: Recommends where the user should eat, using their Gourmet Trails history, ratings, wishlist and taste profile, and checks that the places are real and open. Use when the user asks "where should we eat tonight?", "brunch this Sunday?", "somewhere new near work for lunch", "a cuisine I haven't tried", "date night in town", "what's good near the station?", or "which wishlist place should we do this weekend?".
---

# Recommend a place to eat

**Page first:** follow `${CLAUDE_PLUGIN_ROOT}/references/page-setup.md` to find or create the
user's Gourmet Trails page (PAGE). Data model:
`${CLAUDE_PLUGIN_ROOT}/skills/gourmet-log/references/data-model.md`.

## Steps

1. **Read the context** (`url` = PAGE): `places` (all) and `meta/profile`. Note:
   - top-rated places and their cuisines (what they love),
   - low-rated places (what to avoid repeating),
   - wishlist places (already chosen by the user, so these come first),
   - cuisines not yet stamped (the passport motivates new stamps).
2. **Pin down the request** from the user's message: when (tonight, Sunday brunch), where (city
   or neighbourhood; default to `homeBase` from the profile), who with, and budget. Ask one
   question only if the answer would change the picks completely (e.g. city unknown and no
   home base saved).
3. **Build candidates**:
   - Wishlist places that fit the occasion and area.
   - New places found by web search that match their loved cuisines or fill a missing stamp.
   - At most one repeat favourite when the occasion suits a safe choice.
   Check every candidate on the web: it exists, it is open at that time, and roughly what it
   costs. Drop anything you can't confirm.
4. **Answer with 2–3 picks**, best first. For each: name, area, why it fits them (tie it to
   their actual history: "you rated Saffron House 5, this is the Kerala-style place people
   compare it to"), what to order, and whether it earns a new passport stamp. Keep it short.
5. **Offer to add** the new picks to the wishlist; when the user says yes, write them with
   `gourmet-log` conventions (`status: "wishlist"`, `toTry`, `source: "Suggested by Claude"`).

## Judgement

- Opening hours, closures and prices change: always look them up.
- Don't recommend a place the user rated 1–2 unless they ask.
- If the profile is empty, recommend from history alone and suggest the 2-minute taste
  interview (`gourmet-onboard`) once. If both are empty, ask for the city and one cuisine they
  like, and recommend from the web.
- End with sources for facts you looked up.

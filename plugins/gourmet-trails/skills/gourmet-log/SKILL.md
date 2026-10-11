---
name: gourmet-log
description: Adds and updates restaurants on the user's Gourmet Trails page — visits with dish photos, wishlist places from a Google Maps link or a name, ratings, notes, names for unnamed places, and removals. Use when the user says "dinner at Hoshi Izakaya last night", sends food photos, "add Casa Nopal to my list", pastes a maps.app.goo.gl link, "the tapas photos are from Bar Alfama", "rate Saffron House 5", "we finally went to Blue Nile Kitchen", or "remove the kebab place".
---

# Log a restaurant

**Page first:** follow `${CLAUDE_PLUGIN_ROOT}/references/page-setup.md` to find or create the
user's Gourmet Trails page (PAGE). Read `references/data-model.md` before the first write in a
conversation. For photos, follow `references/photo-workflow.md`.

Load `ArtifactData` with ToolSearch (`select:ArtifactData`) if it is not loaded.

## Steps

1. **List the current places** (`ArtifactData` `list`, `url` = PAGE, collection `places`,
   limit 200) so you can match names, reuse cuisine labels, and get each document's `version`.
2. **Work out what the user wants**:
   - **A visit** ("dinner at X", photos of food): find the place or create it with
     `status: "visited"`. Append a `visits` entry (date from the user's words or photo
     metadata; "last night" → yesterday's date, using today's date from the conversation or a
     time tool), add dishes, set `lastVisit`. If it was on the wishlist, flip `status` to
     `"visited"` and keep `toTry`.
   - **A wishlist place** (a name, or a Google Maps link):
     - For a link, `WebFetch` it to get the name and address. Short `maps.app.goo.gl` links
       often fail to resolve; if so, ask the user for the name instead of guessing.
     - Web-search the place to confirm it exists and is open, its neighbourhood, city and
       cuisine, and 2–3 dishes reviewers and the menu point to. Put them in `toTry`, best first.
     - Set `source` ("Google Maps link" / "Added by name") and `mapsUrl`.
   - **A name for a placeholder** ("the tapas photos are from …"): update `name`, set
     `needsName: false`, look up `area`, `city`, `address`, `mapsUrl`. If the real place already
     exists as its own document, merge the placeholder's photos and dishes into it and delete
     the placeholder.
   - **A rating or note**: write only what the user said. Ratings are 1–5; never infer one from
     enthusiasm. Notes are the user's words, lightly tidied.
   - **Removal**: confirm which place in one line, then `delete` it. Leave its photos in the
     asset store unless the user asks to delete them too.
3. **Write** with `update` (existing, pinned with `if_version`) or `set` (new). Use one `batch`
   for several places.
4. **Reply briefly**: what changed, any "Name needed" places left, and one useful follow-up
   only if there is a real one (e.g. "Want a share card for it?"). Don't paste the page URL
   (except the one-time link when the page was just created); use `Artifact`
   `action: "open"` if the user should see the page now.

## Judgement

- One restaurant, one document. Repeat visits add to `visits` and `photos`; they never create
  a second card.
- When a photo's restaurant is ambiguous, ask rather than guess. A wrong name on a card is
  worse than a "Name needed" badge.
- Keep cuisine labels consistent; the passport counts distinct labels.
- Prices, opening hours and "still open" facts change: look them up, don't recall them.

---
name: suggest-outfit
description: Suggests outfits for a specific event from the pieces the user actually owns, using their logged wardrobe, color pairings and outfit history. Use when the user asks "what should I wear to the office tomorrow", "outfit for a wedding on Saturday", "date night outfit", "plan my outfits for this week", or "what goes with my olive chinos".
---

# Suggest an outfit

Build outfits only from the user's recorded wardrobe in the database of their private **Wardrobe** page (use `ArtifactData`; load via ToolSearch `select:ArtifactData` if deferred). Field meanings are in `references/data-model.md`; pairing rules and the user's colouring preferences are in `references/color-guide.md`.

**First:** find or create the Wardrobe page by following `${CLAUDE_PLUGIN_ROOT}/references/page-setup.md`.

## Workflow

0. **Multi-function events**: if the event has several functions or dress codes (e.g. an Indian wedding with haldi, mehendi, sangeet, ceremony, reception), use the plan-event skill instead.
1. **Pin down the brief** from the request: event type, date, and any constraints (dress code, venue, weather, a piece the user wants to wear). Ask one short question only if the event type is unclear. For a wedding, ask whether it is a Western or Indian/traditional ceremony if not obvious, since it changes the options.
2. **Load data**: `list` `items`, `outfits`, `combos` and `outfit_ideas`, and `get` `profile/me`.
3. **Check the weather when the date is within ~7 days**: use the location named in the request, else `home_city` from `profile/me`. If neither is known, ask for the city once (and save it to the profile), or skip the forecast with a one-line note. Use web search for the forecast and let it steer fabric and layers.
4. **Filter candidates**:
   - Formality matches the event (office 3–4, casual 2, date 3, wedding 4–5, formal 5); all pieces within one step of each other.
   - Season suits the date.
   - Prefer pieces tagged with the event in `occasions`.
5. **Compose 2–3 options**, each with top, bottom (or suit/dress/traditional), footwear, optional outerwear and 1–3 accessories:
   - Never use a color pairing marked `avoid` in `combos`; favor `works` pairings.
   - Near the face, favor the profile's `flattering_colors` and keep `colors_to_avoid` away (see `color-guide.md`).
   - Avoid repeating the exact same outfit worn in the last 14 days, and avoid wearing the same statement piece to the same type of event twice in a row.
   - Match belt to shoes.
   - Give one option that uses a rarely or never worn piece when it fits.
6. **Present** each option as a short block: name (e.g. "Tonal navy"), the pieces by name, why it works in one line, and the accessory call. Lead with the recommended one.
7. **Save the ideas**: write each presented option to `outfit_ideas` (one `batch`) with `name`, `event`, `item_ids`, `why`, `created` (now) and `status: "idea"`, so the page shows them under "Recent outfit ideas". Add `wada_no`/`wada_colors` only when an option clearly follows a known Sanzo Wada combination.
8. **Offer to log**: after the user picks one, set that idea's `status` to `picked` and save it to `outfits` with `status: "planned"` (or `worn` if they say they wore it), following the log-wardrobe conventions.

## Gaps

If the wardrobe lacks something essential for the event (e.g. no formality-5 pieces for a black-tie wedding), say so plainly, give the closest option, and suggest what to borrow or buy — briefly, without a full shopping analysis.

If the wardrobe is empty or nearly empty, say so and offer to log pieces first; give generic advice only if the user asks for it.

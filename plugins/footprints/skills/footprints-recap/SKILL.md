---
name: footprints-recap
description: Turns the user's Footprints data into short animated travel recaps — a year-in-travel film with flight arcs from their home city, a postcard reel for one trip, or a route teaser before a trip. Use when the user says "make my travel recap", "year in travel video", "animate my Portugal trip", "make a reel of Kyoto for Instagram", or "a teaser for my Marrakech trip".
---

# Animated recaps

First get the page URL with `${CLAUDE_PLUGIN_ROOT}/references/page-setup.md` (find the page titled "Footprints", or create it on first run). Then read `references/schema.md`, then read only the collections the recap needs. A year-in-travel film needs `profile/travel.home` for its arcs; if it's missing, ask once as `references/schema.md` describes, or draw the arcs from stop to stop instead.

## Pick the recap

| Ask | Data | Story |
|---|---|---|
| Year in travel | `places` with `from` in the year, plus `profile/travel.home` | Globe or flat map; arcs draw from home to each place in date order; country and km counters tick up; each stop shows name, month and caption; ends on the totals. |
| One trip | one or more `places` pins + `notes` | Title card, route between stops, a beat per highlight, closing line from the caption. |
| Teaser | a `trips` doc | Route animates day by day with the day titles; ends on the countdown to `start`. |

Only public fields (`name`, `country`, `caption`, `highlights`, dates) go into anything meant for sharing. Ask before using anything from `notes` or `trips`. The home city is private profile data: ask before naming it on screen in a recap meant for sharing (otherwise label it "Home").

## Make it

1. Draft the storyboard in chat: 5–9 beats, each with on-screen text (short) and duration. Total 15–30 s for Instagram, up to 60 s otherwise. Format: 9:16 for Reels/Stories, 16:9 otherwise. Ask which if they didn't say.
2. Build it with the best available route, in this order:
   - A video tool the user has connected or installed. For example, the **HyperFrames (HeyGen)** connector: `compose` a new project from the storyboard, with the data inlined as text (places, dates, coordinates, captions), then render to MP4 with `render_video` (load its tools with ToolSearch). In Claude Code, where hosted compose may be disabled, use local HyperFrames or Remotion skills if they're installed, writing the composition into the user's working directory.
   - A `Motion` artifact type, if the `Artifact` types listing has one.
   - Otherwise a self-contained animated HTML artifact (SVG map with d3 from cdnjs, CSS/JS timeline, play/replay button). The user can screen-record it. The Footprints page's own "Play journey" button on the globe is also a quick live option.
3. Photos: the page stores the user's uploads in `photos/{id}` as data URLs. Use them only if they ask; never pull photos from the web.
4. Deliver with one line on length and format, and offer one change (pace, music-free cut, different format).

## Rules

- Keep text on screen short enough to read at speed: about 6 words per beat.
- No real people's faces or copyrighted music, logos or footage.

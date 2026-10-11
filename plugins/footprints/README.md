# Footprints

A travel atlas that you and Claude keep together on one private page. **Visited** shows a spinning globe (or flat map) with a pin for every place you've been, countries tinted, arcs from your home, and a journal. Tap a pin to see the dates, a caption, highlights and private memories that only you can see. **Bucket list** shows illustrated postcards of places you want to go, with the best season and a priority. **Plan** holds a day-by-day itinerary for each trip, tickets to book with book-by dates, a packing checklist, and your travel profile. Claude does the interviewing, logging, planning and recommending in chat and writes the results to the page.

## Skills

| Skill | Say something like |
|---|---|
| `footprints-onboard` | "Interview me for Footprints" |
| `footprints-log-trip` | "I just got back from Porto" |
| `footprints-bucket-list` | "Add Patagonia to my bucket list" |
| `footprints-plan-trip` | "Plan 5 days in Morocco in May" |
| `footprints-recommend` | "Where should I go next?" |
| `footprints-recap` | "Make my travel recap for this year" |

## Install

```
/plugin marketplace add benchlog-ai/plugins
/plugin install footprints@benchlog
```

## First run

The first time you use any Footprints skill, Claude looks for an artifact of yours titled **Footprints**. If there isn't one, it publishes a fresh, empty copy of the page (bundled in `assets/page.html`) as a private artifact and gives you the link. After that, every skill finds and uses that page. Start with "interview me for Footprints" so Claude learns your home city and airport, which it uses for flight searches, arcs on the map and public holidays.

## Privacy

Your data stays on your own private page in your Claude account. Nothing is sent to Bench Log. If you share the page, viewers see only the map, short captions and your bucket list. Private memories, trip plans, tickets and your travel profile (including your home city) stay hidden by the page's access rules.

## Requirements and limits

- The page needs Claude artifacts with the `db` and `user` capabilities, so it runs inside claude.ai or the Claude apps.
- Flight and stay searches use the Kiwi.com and Booking.com connectors if you have them connected. Claude searches but never books or pays.
- Animated recaps use a video tool if you have one (for example the HyperFrames connector, or HyperFrames/Remotion skills in Claude Code). Otherwise Claude makes an animated HTML page you can screen-record.
- Photos you upload are stored in the page's database, downscaled, and count toward its storage limit.

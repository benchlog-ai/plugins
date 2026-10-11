# Wardrobe Tracker

A wardrobe Claude remembers. You tell Claude what you own (in words or with a photo), what you wore and which color pairings work for you, and it keeps the record on a private page called **Wardrobe** that updates live: a color palette, your pieces as swatches, recent outfits, rated pairings, outfit ideas and a ranked list of what to buy next. Claude then uses that record to suggest outfits from what you actually own, plan multi-function events such as an Indian wedding on a separate page you can share with family, and point out what you wear most and what you ignore.

## Skills

| Skill | Example |
|---|---|
| **log-wardrobe** — add pieces and accessories, log outfits worn, rate color pairings | "Add my navy wool blazer" |
| **suggest-outfit** — 2–3 outfits for an event from what you own, checking the forecast for near dates | "What should I wear to the office tomorrow?" |
| **plan-event** — dress code, color theme and outfit per function, with family color coordination, published as a shareable event page | "Plan my outfits for my cousin's wedding" |
| **wardrobe-insights** — color balance, most and least worn pieces, go-to combinations, occasion coverage | "Give me a wardrobe review" |
| **shopping-gaps** — ranked list of what to buy next to unlock the most new outfits | "What should I buy next?" |

## Install

```
/plugin marketplace add benchlog-ai/plugins
/plugin install wardrobe-tracker@benchlog
```

## First run

The first time you use any skill, Claude looks for a page titled `Wardrobe` among your artifacts. If there isn't one, it publishes a fresh, empty Wardrobe page to your claude.ai account, gives you the link once, and asks a few optional questions (your city and timezone for weather and dates, and if you like, your colouring and colors you love or avoid). After that every skill reads and writes that same page. Don't rename it, or Claude will not find it and will make a new one; if that happens, paste the page link into the chat.

## Privacy

Your data stays on your own private page in your claude.ai account. Nothing is sent to Bench Log. Event pages made by plan-event are also private until you share them from the page's Share menu; they only show the event plan, never your full wardrobe. People you share an event page with need to sign in to claude.ai to see it.

## Requirements and limits

- Needs Claude with Artifacts and artifact databases (the `Artifact` and `ArtifactData` tools), as in the Claude desktop app or Claude Code signed in to claude.ai.
- Weather checks and shopping links use web search when it is available.
- The pieces, colors and pairings are only as good as what you log; Claude never invents pieces you didn't mention or show.
- The Indian wedding guide is a general starting point; your family's dress code always wins.

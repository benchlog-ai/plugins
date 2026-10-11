# Larder

Larder lets Claude look after your kitchen through one private page: drawn pantry and fridge shelves, a weekly meal calendar and a shopping checklist, all on one live database. You see and edit the page in your browser; Claude edits the same data from chat. Cook a planned meal and the ingredients come off the shelves; tick an item on the list and it goes onto the shelves.

## Skills

| Skill | What it does | Try saying |
| --- | --- | --- |
| `larder-pantry` | Add, remove and adjust stock; what is low or needs using soon | "I used the last of the cumin" |
| `larder-plan` | Suggest balanced, seasonal or new-cuisine meals, fill the week, mark meals cooked and take the ingredients off the shelves | "Plan my dinners for this week" |
| `larder-shop` | Build the grocery list from the plan and low stock, mark items bought (which stocks the pantry), clear the list | "Make my grocery list" |

## Install

```
/plugin marketplace add benchlog-ai/plugins
/plugin install larder@benchlog
```

## First run

The first time you use any Larder skill, Claude looks for a page titled "Larder" in your artifacts. If there is none, it publishes a fresh, empty Larder page as a private artifact in your account and gives you the link. It then asks three short questions (where you shop, any diet or foods you avoid, how many people you cook for) so meal ideas fit you. After that, every skill uses the same page.

## Privacy

Your pantry, meal plan, list and kitchen settings live only on your own private page in your Claude account. Nothing is sent to Bench Log. You can share the page with your household from its Share menu if you want to.

## Requirements and limits

- Needs Claude with Artifacts and the artifact database (claude.ai, the Claude desktop app or Claude Code signed in to claude.ai).
- The page's "Ask Claude for ideas" button uses your own Claude usage and asks for permission the first time.
- Seasonal and "trending" ideas use web search when it is available; otherwise they come from general knowledge, and Claude says so.
- Shelf drawings are simple shapes picked from the item name, not photos.

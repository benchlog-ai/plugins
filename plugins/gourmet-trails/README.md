# Gourmet Trails

A restaurant log that Claude keeps for you on one private page. Tell Claude where you ate, send
dish photos, paste a Maps link for a place you want to try, or forward a friend's tip, and it
lands on the page: restaurants grouped by cuisine (or by rating or recency) with your own dish
photos, a Want to go list with dishes to try, Best of lists, a flavour passport of the cuisines
you have tried, and a Share button that makes a recommendation card. Claude also uses the log to
suggest where to eat next.

## Skills

| Skill | What it does | Try saying |
|---|---|---|
| gourmet-onboard | Creates your page, runs a short taste interview, and imports past visits from photos or a list | "Set up Gourmet Trails" |
| gourmet-log | Visits with dish photos, wishlist places from a Maps link or a name, ratings, notes, names for unnamed places | "Dinner at Hoshi Izakaya last night" + photos |
| gourmet-recommend | Picks 2–3 places from your history, wishlist and taste profile, checked on the web | "Where should we eat Saturday?" |
| gourmet-photos | Scans the Mac Photos library for food photos, names the restaurant from the photo's location, adds the meal with captioned dishes, and tags the photos in Photos | "Check my photos for restaurants since September" |
| gourmet-share | PNG share cards, Best of lists, and a one-image list card to send friends | "Make a share card for Saffron House" |
| gourmet-friends | Friends' recommendations onto your wishlist, marked with who sent them | "Maya says try Casa Nopal" |

## Install

```
/plugin marketplace add benchlog-ai/plugins
/plugin install gourmet-trails@benchlog
```

## First run

The first time any Gourmet Trails skill runs, Claude looks for an artifact of yours titled
"Gourmet Trails". If there is none, it publishes a fresh, empty page from the template bundled
with the plugin and gives you the link once. The page is private to you. Every later
conversation finds the same page by its title, so keep the title as it is.

## Privacy

Your restaurants, photos and taste profile stay on your own private page in your claude.ai
account. Nothing is sent to Bench Log. Photos are resized and saved as new JPEGs before upload,
which drops GPS and other metadata. Allergies and health conditions are never stored.
`gourmet-photos` looks restaurants up on OpenStreetMap (Nominatim, Overpass) by sending the
coordinates of each meal; nothing else leaves your Mac except the uploaded dish photos.

## Requirements and limits

- The page needs claude.ai artifacts with a database and an asset store (the skills create it
  for you).
- `gourmet-photos` is **macOS only**: it needs the Photos app, `python3`, and your permission
  for Claude to control Photos (System Settings › Privacy & Security › Automation). On other
  systems, send photos in chat instead.
- The share-card scripts need Python 3 with Pillow (`pip install pillow`).
- Restaurant facts (opening hours, prices, closures) are looked up on the web each time and can
  still be out of date.

## Credits

The share cards use Bodoni Moda, Karla and DM Mono, licensed under the SIL Open Font License
1.1 (see `skills/gourmet-share/assets/OFL.txt`).

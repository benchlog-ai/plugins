# Adding dish photos

1. **Find the files.** Photos attached in chat are available by name in the session (also as
   files under the uploads folder). Photos in a folder on the user's computer: stage them into
   the workspace first. For the Mac Photos library itself, use the `gourmet-photos` skill
   (macOS only): it finds, groups, names and tags meals there.
2. **Read the metadata before resizing.** Run a short Python/Pillow script that prints, for
   each photo: `DateTimeOriginal` (EXIF 36867), GPS latitude/longitude, and camera model.
   Chat uploads usually have metadata stripped; when there is none, say so once and rely on
   what the user tells you.
3. **Group photos into visits.** Same evening + same place (GPS within ~80 m, or matching
   tableware, table surface, placemats, coasters, menus in the frame) = one visit. Look for
   names printed on coasters, placemats, boards, menus or receipts; they are the strongest clue
   to the restaurant (e.g. a coaster printed with the restaurant's name). Branded items can
   mislead too: a cutting board or glass brand is not necessarily the restaurant.
4. **Identify the restaurant.**
   - GPS present: search the web for restaurants at those coordinates and match the cuisine
     you see on the plate. Never write the coordinates into the records or the reply.
   - A name clue in the frame: web-search "<clue> restaurant <city>" to confirm the name,
     address and neighbourhood.
   - Nothing to go on: create the place with `needsName: true` and a descriptive placeholder
     name ("Tapas restaurant"), and ask the user which restaurant it was.
   Never present a guessed restaurant name as fact; say how sure you are.
5. **Recognise the dishes.** Caption each photo with the dish you see, concretely
   ("Pinchos morunos on bread", "Thali with rasam, vadas and payasam"). Set `cuisine`, add
   dishes to `dishes`, and pick `order` (the dish that best represents the place).
6. **Prepare the files.** For each photo: apply EXIF orientation, convert to RGB, resize so the
   long side is 1400 px, save as JPEG quality 82. Saving a new JPEG drops the GPS metadata,
   which is what we want for anything that might be shared.
7. **Upload.** `Artifact` with `url` = PAGE, `asset: true`, `file_paths` = up to 25 files per
   call. Keep the returned `id` and `url` for each file exactly as given.
8. **Write the records.** Merge into the existing place (append to `photos`, `dishes`,
   `visits`) or create a new one, following `data-model.md`. Set `cover` to the most
   appetising, best-lit photo, unless the user picked one.
9. **Confirm in one or two lines**: what was added where, which names are still needed, and
   which dish identifications you are unsure about.

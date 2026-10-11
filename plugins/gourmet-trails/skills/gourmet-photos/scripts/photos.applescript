-- Gourmet Trails bridge to the Mac Photos app.
--   find   <fromYYYYMMDD> <toYYYYMMDD> <search term>   -> one line per photo: id TAB filename TAB date TAB lat TAB lon TAB keywords
--   export <posix out dir> <id> [<id> ...]              -> exports JPEGs (current edited version)
--   tag    <keyword|keyword> <id> [<id> ...]            -> adds keywords, keeps existing ones
on run argv
	set cmd to item 1 of argv
	if cmd is "find" then return findPhotos((item 2 of argv) as integer, (item 3 of argv) as integer, item 4 of argv)
	if cmd is "export" then return exportPhotos(item 2 of argv, items 3 thru -1 of argv)
	if cmd is "tag" then return tagPhotos(item 2 of argv, items 3 thru -1 of argv)
	error "unknown command " & cmd
end run

on pad(n)
	if n < 10 then return "0" & n
	return n as string
end pad

on findPhotos(fromDay, toDay, term)
	set out to ""
	tell application "Photos"
		set ps to search for term
		repeat with p in ps
			set pd to date of p
			set k to (year of pd) * 10000 + (month of pd as integer) * 100 + (day of pd)
			if k ≥ fromDay and k ≤ toDay then
				set t to time of pd
				set iso to ((year of pd) as string) & "-" & my pad(month of pd as integer) & "-" & my pad(day of pd) & "T" & my pad(t div 3600) & ":" & my pad((t mod 3600) div 60) & ":" & my pad(t mod 60)
				set la to ""
				set lo to ""
				try
					set loc to location of p
					set la to (item 1 of loc) as string
					set lo to (item 2 of loc) as string
				end try
				set kw to ""
				try
					set ks to keywords of p
					if ks is not missing value then
						set AppleScript's text item delimiters to "|"
						set kw to ks as string
						set AppleScript's text item delimiters to ""
					end if
				end try
				set out to out & (id of p) & tab & (filename of p) & tab & iso & tab & la & tab & lo & tab & kw & linefeed
			end if
		end repeat
	end tell
	return out
end findPhotos

on exportPhotos(outDir, ids)
	set items_ to {}
	tell application "Photos"
		repeat with i in ids
			set end of items_ to media item id (i as string)
		end repeat
		export items_ to (POSIX file outDir as alias) without using originals
	end tell
	return (count of items_) as string
end exportPhotos

on tagPhotos(kwArg, ids)
	set AppleScript's text item delimiters to "|"
	set newKw to text items of kwArg
	set AppleScript's text item delimiters to ""
	tell application "Photos"
		repeat with i in ids
			set p to media item id (i as string)
			set cur to keywords of p
			if cur is missing value then set cur to {}
			repeat with k in newKw
				if (k as string) is not in cur then set end of cur to (k as string)
			end repeat
			set keywords of p to cur
		end repeat
	end tell
	return (count of ids) as string
end tagPhotos

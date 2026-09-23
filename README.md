# APClassProject
 A project for my Advanced Programming class

# Photo Duplicate Finder

## 1. The demo

I run `find-duplicates photos/` in a terminal. It scans x images and
prints: "3 exact duplicates found, 5 near-duplicate groups found." It
writes `duplicates_20260923_1430.xlsx` next to the folder (the date and
time of the run, so a rerun doesn't silently overwrite an earlier
report — if that exact filename ever already exists, I'm asked to
confirm before it's overwritten) — one table per group, listing the
filenames in that group and a similarity score, with the suggested file
to keep (the largest or highest-resolution copy) highlighted. I open the
spreadsheet and see a table for a group of four files — a burst of
near-identical shots — with IMG_0231.jpg highlighted as "keep" and the
other three left unhighlighted.

## 2. The shape

in            a folder of image files (.jpg, .png)
out           an Excel report: one table per duplicate/near-duplicate
              group, listing the files in the group, a similarity score,
              and a suggested file to keep (highlighted)
in between    hash each file to catch exact duplicates; compute a
              perceptual similarity measure between remaining images to
              catch near-duplicates; group images whose similarity
              exceeds a threshold; pick a "keep" candidate per group by
              file size or resolution

## 3. The size

First useful version
- scans a single folder (not recursive subfolders) of .jpg and .png files
- detects exact duplicates via file hash
- detects near-duplicates via a perceptual similarity measure, within a
  configurable threshold
- groups matches and suggests one file to keep per group
- outputs one Excel report + a printed summary count

Not this term
- recursive folder scanning
- automatically deleting or moving files
- detecting rotated, cropped, or heavily edited duplicates
- video file support
- a graphical interface for reviewing groups (Excel output only)
- cloud storage integration (Google Photos, iCloud, etc.)

## 4. How we would know it works

- Given two byte-identical files, they are grouped as exact duplicates.
- Given two unrelated photos, they are not grouped together.
- Given a photo and a resized (but otherwise identical) copy of it, they
  are grouped as near-duplicates — and this is checked as an explicit
  test case, not assumed to work.

## 5. What could stop this

- Personal photo libraries can contain sensitive images. The project
  will be built and demoed using a small sample folder of non-sensitive
  images (e.g. public domain or self-taken test photos), not a real
  personal library.
- In real life it can be hard to identify photos based on their filename only which are often complicated
- Perceptual similarity detection is the main technical risk: choosing
  and tuning a similarity measure that reliably separates "near-duplicate"
  from "just similar" has not been tried before, and should be tested
  early against known cases (rotated copies, resized copies, unrelated
  photos) rather than assumed to work. Not to mention my lack of experience in the field
- Performance on large folders (thousands of images) is untested; the
  first version is scoped to folders in the low hundreds at best.
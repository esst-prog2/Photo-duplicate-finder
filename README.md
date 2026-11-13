# APClassProject
 A project for my Advanced Programming class

# Photo Duplicate Finder

## 1. The demo

I run `find-duplicates photos/` in a terminal. The folder holds a photo,
IMG_0231.jpg, and three copies of it: a byte-identical copy, a copy resized
smaller, and a copy saved again at lower quality. The tool reads the .jpg,
.jpeg and .png files in that folder (not in its subfolders) and prints one
line:

    1 exact duplicates found, 1 near-duplicate groups found.

That is one group, counted twice. "Exact duplicates" counts the sets of
files that are byte-for-byte identical (here the photo and its copy), and
"near-duplicate groups" counts the reported groups whose files are not all
byte-identical (here all four). A group that mixes both kinds is counted in
both numbers, so the two numbers do not add up to the number of tables in
the report.

It writes `duplicates_20260923_1430.xlsx` next to the folder (the date and
time of the run, so a rerun doesn't silently overwrite an earlier report —
if that exact name already exists I'm asked to confirm, and pressing Enter
means no). I open the spreadsheet and see one table per group. This one
lists the four files with a "Similarity" column, which says Exact when all
the files are byte-identical and otherwise Very Similar or Similar, and has
IMG_0231.jpg highlighted as the file to keep; the other three rows are left
unhighlighted. The file to keep is the one with the largest file size.
Resolution only decides between files of equal size, and between files that
are equal in both, the one that comes first by name wins (which is why the
original and not its identical copy is highlighted).

Two more things the tool does. If the folder holds photos in a format it
does not read (for example .heic), a warning on the error stream says how
many were skipped, instead of a silently empty result. And `--threshold N`
sets how alike two photos must look to be grouped: 0 means only photos that
look identical, larger values group looser matches, and the default is 8.
Very large values lump unrelated photos together.

## 2. The shape

in            a folder of image files (.jpg, .jpeg, .png)
out           an Excel report: one table per duplicate/near-duplicate
              group, listing the files in the group, a similarity category,
              and a suggested file to keep (highlighted)
in between    hash each file to catch exact duplicates; compute a
              perceptual similarity measure between remaining images to
              catch near-duplicates; group images whose similarity
              exceeds a threshold; pick a "keep" candidate per group by
              file size or resolution

## 3. The size

First useful version
- scans a single folder (not recursive subfolders) of .jpg, .jpeg and .png files
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

## 6. Setup and versions

Tested with Python 3.11.15. Every Python package this project imports is
pinned to an exact version in `pyproject.toml`. The three packages that
`imagehash` pulls in on its own (numpy, scipy, PyWavelets) are not pinned;
the benchmark test would show it if a new release of them changed the hashes.
To set up:

    python -m venv .venv
    .venv\Scripts\python -m pip install -e ".[dev]"
    .venv\Scripts\python -m pytest

The specs under `openspec/` are managed with the OpenSpec command line tool,
which is not a Python package: `npm install -g @fission-ai/openspec@1.13.0`
(installed with Node 20.14.0, where npm warned that one of its own
dependencies prefers 20.17 or newer, and it worked anyway; that installed
version also runs on Node 26.12.1, but the install command itself was not
repeated on 26.12.1).


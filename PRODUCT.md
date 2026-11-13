# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack
Plain static HTML and CSS (the user's choice). Hosting is undecided; the page is a file in the repo for now, and publishing it (for example with GitHub Pages) is a later step.

## Users
Classmates and the teacher of an Advanced Programming class. They read the page in under a minute to see what the tool does, that it works, and where it stops. The alternative they know is sorting a photo folder by hand.

## Product Purpose
Photo Duplicate Finder is a Python command-line tool (`find-duplicates`) that scans a folder of photos and writes an Excel report: one table per group of look-alikes, the best copy highlighted. The promo page introduces it to those readers. Success: a classmate can say in their own words what the tool does and what it cannot do.

## Positioning
Every claim on the page can be checked: a planted benchmark, tests that fail on purpose, a mutation test, a planning log and a process log. The page also says what the tool misses, with a real measurement on one folder of the author's own photos.

## Operating Context
The reader sees the page on GitHub or in a browser, as part of a class project review. The tool itself runs in a terminal and its output is an Excel file. It reads .jpg, .jpeg and .png in one folder (no subfolders), and warns about skipped formats such as .heic.

## Capabilities and Constraints
- The page content is fixed and approved: `docs/promo-page.md`, from the design doc `docs/designs/promo-page-content.md`. Copy changes need the user's decision.
- No exact counts are promised for a reader's folder. The one exception is a single scoped line about one real-folder run (`docs/measurements/real-folder-run-2026-11-13.md`).
- Test results appear in words, scoped to the test set.
- Only facts already verified in the repo. Mirrored, turned, bordered or cropped copies are expected to be missed (README "Not this term").
- Different shots of one scene were never tested, so nothing is claimed about them.
- The action the page serves: the reader runs the command on their own photos.
- One page, desktop and phone widths. It links out to the spec, planning log and process log and does not reproduce them.

## Evidence on Hand
- Approved page text: `docs/promo-page.md`.
- Real-folder measurement: `docs/measurements/real-folder-run-2026-11-13.md`.
- Planted benchmark photos: `benchmark/data` (80 files, the author's own photos in a public repo). Whether any appear on the page is an open decision.
- Absent: screenshots of the Excel report, testimonials, customer names, and any hosting or domain. Do not invent them.

## Product Principles
- Give the full picture of performance: what it finds, what it misses, and how that was measured.
- Every statement traces to a test, a commit or a log entry.
- Lead with the result, then the proof.
- Promise no count the reader's own folder might not give.
- Honest about its limits, with no marketing gloss.

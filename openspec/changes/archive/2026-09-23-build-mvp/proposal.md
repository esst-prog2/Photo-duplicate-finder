## Why

The project currently has only a README describing the intended tool; no code exists.
We need a first working version of the Photo Duplicate Finder so it can be demoed and
tested against the acceptance criteria already agreed in README.md (exact duplicates,
near-duplicates via resizing, unrelated photos not grouped).

## What Changes

- Add a CLI (`find-duplicates <folder>`) that scans a single, non-recursive folder of
  `.jpg`/`.png` files.
- Detect exact duplicates via a file-content hash (SHA-256).
- Detect near-duplicates via a perceptual hash (Hamming distance) within a
  configurable similarity threshold.
- Merge exact and near-duplicate matches into groups and pick one "keep" candidate
  per group (largest file size / highest resolution).
- Write `duplicates.csv` next to the scanned folder and print a summary count
  (e.g. "3 exact duplicates found, 5 near-duplicate groups found.").
- Add a small checked-in fixture set of synthetic (non-personal) test images —
  identical copy, resized copy, unrelated image — to test against the criteria in
  README.md section 4.

Out of scope for this change (per README "Not this term"): recursive folder
scanning, auto-delete/move, rotated/cropped duplicate detection, video support, a
GUI, cloud storage integration.

## Capabilities

### New Capabilities
- `photo-scanning`: discover `.jpg`/`.png` files in a single folder (non-recursive).
- `exact-duplicate-detection`: identify byte-identical files via content hash.
- `near-duplicate-detection`: identify visually-similar-but-not-identical files via
  perceptual hash and a configurable similarity threshold.
- `duplicate-report`: merge exact/near-duplicate matches into groups, choose a keep
  candidate per group, and emit the CSV report plus printed summary.

### Modified Capabilities
(none — greenfield project)

## Impact

- New Python package (`find_duplicates/`) and CLI entry point.
- New dependencies: Pillow, imagehash, click (runtime); pytest (dev/test).
- New `tests/` directory with a `fixtures/` folder of small synthetic images.
- No existing code, specs, or systems are affected.

## Context

Greenfield project — no existing code. See proposal.md for motivation and specs/
for the behavior contract. This document covers the technical approach: language,
libraries, module boundaries, and the algorithm for turning a folder of images into
`duplicates.csv`.

## Goals / Non-Goals

**Goals:**
- A working `find-duplicates <folder>` CLI that satisfies specs/photo-scanning,
  specs/exact-duplicate-detection, specs/near-duplicate-detection, and
  specs/duplicate-report.
- Keep the riskiest piece — perceptual similarity tuning — isolated in one module
  that can be tested and retuned independently of scanning/grouping/reporting.
- Testable against the explicit cases from README.md section 4: identical files,
  resized copy, unrelated photos.

**Non-Goals:**
- Performance at folder sizes beyond a few hundred images (README explicitly scopes
  this out for v1).
- Any implementation-level optimization (bucketing/indexing for near-duplicate
  comparison) beyond a straightforward pairwise comparison — acceptable at MVP
  scale; can be revisited later without a spec change.

## Decisions

**Language/runtime: Python 3.11+.**
Rationale: image libraries (Pillow, imagehash) are mature and simple; a class MVP
doesn't need a compiled toolchain. Alternative considered: a Node.js CLI using
`sharp` + a perceptual hash package — rejected because Python's imaging ecosystem
is more battle-tested for this exact use case.

**Exact-duplicate detection: SHA-256 over file bytes (`hashlib`, stdlib).**
Rationale: simplest possible correct implementation of specs/exact-duplicate-detection;
no dependency needed. Files are grouped by identical digest.

**Near-duplicate detection: perceptual hash via the `imagehash` library (average
hash, `ahash`), compared with Hamming distance against a configurable threshold.**
Rationale: `ahash` is simple, fast, and robust to resizing and mild re-compression —
exactly the case called out in specs/near-duplicate-detection ("a photo and a resized
copy"). Alternative considered: `phash` (DCT-based) — more robust to broader
transformations, but the extra complexity isn't justified for the MVP's explicit
scope (no rotation/crop detection). Can be swapped later since it's isolated in
`hashing.py`.
Default threshold: Hamming distance ≤ 5 (out of 64 bits for an 8x8 ahash) — a
commonly-cited starting point for "likely same image"; exposed via `--threshold` and
tuned against the fixture set in `tests/fixtures/` before being treated as final.

**Comparison strategy: pairwise, O(n²) over files not already exact-matched.**
Rationale: acceptable at the "low hundreds of images" scale this MVP targets (README
section 5). Explicitly a non-goal to optimize further now.

**Grouping: union-find (disjoint-set) over file pairs that match (exact or
near-duplicate).**
Rationale: naturally merges a chain of matches (A≈B, B≈C ⇒ {A,B,C}) into one group,
satisfying specs/duplicate-report's merge requirement, without ad-hoc set-merging
logic.

**Keep-candidate selection: largest file size, tie-broken by highest resolution
(width × height).**
Rationale: matches README's "shape" section directly; file size is a reasonable
proxy for quality/least lossy copy, resolution is the tie-breaker for equal-size
files.

**CLI: `click`.**
Rationale: minimal boilerplate for an argument (`folder`) and an option
(`--threshold`), good `--help` output for a class demo.

**Module layout:**
```
find_duplicates/
  cli.py        # argument parsing, orchestration, prints summary
  scanner.py     # walk folder (non-recursive), filter by extension
  hashing.py      # exact hash (bytes) + perceptual hash (image)
  grouping.py       # union-find over exact/near-duplicate matches
  report.py          # keep-candidate selection, CSV writer
tests/
  test_hashing.py
  test_grouping.py
  test_report.py
  fixtures/            # small synthetic images: base, identical copy, resized
                        # copy, unrelated image (not real personal photos)
```
This mirrors the spec boundaries directly (one module per capability, plus a thin
`cli.py` for orchestration), so each spec file's scenarios map onto one module's
tests.

## Risks / Trade-offs

- **Threshold tuning is unproven** → Mitigation: default is a documented starting
  point, not asserted as correct; the fixture-based test for "resized copy" is what
  validates it, and the threshold is user-configurable so it can be adjusted per
  folder without a code change.
- **O(n²) near-duplicate comparison won't scale past a few hundred files** →
  Mitigation: explicitly a non-goal per README section 5; acceptable for MVP.
- **`ahash` is weaker than `phash` against rotation/crop** → Mitigation: rotation/
  crop detection is explicitly out of scope for this MVP (README "Not this term").

## Open Questions

None — design decisions above are sufficient to start implementation; the threshold
default will be validated (not just assumed) against the fixture tests during
implementation.

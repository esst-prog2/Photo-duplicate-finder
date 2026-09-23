## Why

The report currently shows a raw perceptual-hash Hamming distance in the
"Similarity Score" column. That number is meaningless without knowing the scale
(0-64) and the configured threshold, and it doesn't distinguish an exact
byte-identical match from a near-duplicate that merely scores 0. A person reviewing
the report has to already understand the internals to interpret it.

## What Changes

- Replace the raw Hamming-distance number in the "Similarity Score" column with a
  category label: `Exact`, `Very Similar`, or `Similar`.
- `Exact`: members share an exact byte hash (independent of perceptual distance).
- `Very Similar`: perceptual Hamming distance is in the lower half of the
  configured threshold range (0 up to and including `threshold // 2`).
- `Similar`: perceptual Hamming distance is above that midpoint, up to and
  including the configured threshold (i.e. still matched, but less close).
- The cutoff between "Very Similar" and "Similar" scales with `--threshold`, so it
  never exceeds whatever threshold the user actually ran with.

## Capabilities

### Modified Capabilities
- `duplicate-report`: the "Write an Excel report" requirement's Similarity Score
  column changes from a raw distance number to a three-level category label.

## Impact

- `find_duplicates/cli.py`: `_group_similarity_score()` changes from returning a
  Hamming-distance string to returning a category label, using both exact-hash
  membership and perceptual distance.
- `tests/test_hashing.py`, `tests/test_report.py`, `tests/test_cli.py`: any
  assertions on the numeric score value need updating to the new category labels.
- No change to `report.py`'s `write_report()` itself — `DuplicateGroup.similarity_score`
  stays a string field, just with different contents.

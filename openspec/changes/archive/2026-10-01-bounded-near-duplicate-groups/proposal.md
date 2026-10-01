## Why

Code review and the hw4 spike both confirmed the same defect: `merge_duplicate_groups`
takes the transitive closure of "is within threshold of" (single-linkage/union-find),
but similarity is not transitive. Hamming distance is a true metric, so a chain of
individually-valid matches (A-B, B-C, C-D, ...) can place the chain's ends arbitrarily
far apart, with no upper bound as the chain grows.

The spike ran the current tool against ~300 real, uncurated photos at every threshold
from 0 to 12 (`spike/threshold-spike-results.csv`). The largest group's size explodes
from 2 (threshold 0) to 259 (threshold 12), and even at the "widest safe" threshold of
1, 8 of the 32 reported groups contained a photo that didn't belong. This is the
blob/bridge problem happening on real data, not just a theoretical risk.

Separately, every existing automated test runs on four synthetic PNGs under 3KB with
flat color fills. No test has ever hashed a real photograph (JPEG compression
artifacts, camera noise, realistic resolution), so the threshold and the ahash
approach itself have never been validated against what the tool is actually for.

## What Changes

- Replace single-linkage (transitive closure / union-find) near-duplicate grouping
  with complete-linkage (clique-bounded) grouping: a file only joins a group if it is
  within the configured threshold of **every** current member of that group, not just
  one. This guarantees every reported group's maximum internal pairwise distance is
  at most the configured threshold, regardless of group size.
- Add a small set of real, non-sensitive photographs to the test fixtures (not a
  personal library — per README's existing privacy constraint) and add test cases
  that hash them, exercising the same acceptance criteria (identical, resized,
  unrelated) against real image data instead of only synthetic ones.
- Add a regression test that specifically constructs a chain (each adjacent pair
  within threshold, but the chain's ends far outside it) and asserts the chain is
  split into clique-bounded groups rather than merged into one blob.

## Capabilities

### Modified Capabilities
- `near-duplicate-detection`: the "Detect visually similar files within a threshold"
  requirement gains a bound on multi-file group formation — a group is only valid
  if every pair of its members is within the threshold, not just some chain of pairs.
- `duplicate-report`: the "Merge exact and near-duplicate matches into groups"
  requirement changes from "combine matches that share a file" (transitive) to
  "combine matches into clique-bounded groups" (every member within threshold of
  every other member).

## Impact

- `find_duplicates/grouping.py`: replace the union-find `merge_duplicate_groups`
  with a clique-building clustering function.
- `find_duplicates/cli.py`: `run()` changes how it builds groups — computing
  pairwise perceptual distance directly rather than using the single-linkage
  near-duplicate-pairs + union-find combination.
- `tests/test_grouping.py`, `tests/test_cli.py`: update for the new clustering
  behavior; add the chain-splitting regression test.
- `tests/fixtures/`: add a small number of real photographs (and a real
  resized/recompressed copy, and a real unrelated photo); add corresponding test
  cases in `tests/test_hashing.py`.
- This may change previously-reported group sizes for borderline cases (a file that
  used to ride along in a chain-merged group may now land in a smaller group, or on
  its own) — this is the correctness fix, not a regression.

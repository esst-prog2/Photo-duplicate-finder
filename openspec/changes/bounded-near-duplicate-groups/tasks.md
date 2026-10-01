## 1. Clique-bounded grouping

- [ ] 1.1 Replace `merge_duplicate_groups()` in `grouping.py` with a greedy
  complete-linkage clustering function that only adds a file to a forming group if
  it is within the threshold distance of every current member; verify with a unit
  test that a simple two-file match still groups correctly
- [ ] 1.2 Add a regression test constructing a chain (A-B, B-C, C-D each within
  threshold, A-D not within threshold) and assert A and D never end up in the same
  reported group
- [ ] 1.3 Add a test confirming an exact-duplicate pair merges correctly into a
  near-duplicate clique that one of its members belongs to (verifying the
  triangle-inequality argument from design.md holds in the actual implementation)

## 2. Wire the new clustering into the CLI

- [ ] 2.1 Update `run()` in `cli.py` to compute perceptual hashes once per file and
  use the new clustering function instead of
  `find_near_duplicate_pairs` + `merge_duplicate_groups`; verify the full existing
  test suite still passes (adjusting any assertions that assumed single-linkage
  behavior)
- [ ] 2.2 Run `find-duplicates tests/fixtures/` and manually confirm the report is
  unchanged for the existing (non-chaining) fixture set

## 3. Real-photo fixtures

- [ ] 3.1 Add 2-3 real, non-sensitive photographs to `tests/fixtures/` (a base
  photo, a real resized/recompressed copy, and an unrelated real photo), sourced
  from images the user has rights to use for this
- [ ] 3.2 Add test cases in `tests/test_hashing.py` re-running the exact/near/
  unrelated acceptance checks against the real photos; verify they pass
- [ ] 3.3 Add a test in `tests/test_cli.py` running the full pipeline against a
  folder containing only the real photo fixtures and checking the resulting group
  structure matches expectations

## 4. Documentation

- [ ] 4.1 Note the chaining fix and the spike findings that motivated it in
  PLANNING_LOG.md once implemented (the spike's own findings are already logged;
  this adds the "and here's what we did about it" follow-up entry)

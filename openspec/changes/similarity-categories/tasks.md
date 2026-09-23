## 1. Categorization logic

- [ ] 1.1 Rewrite `_group_similarity_score()` in `cli.py` to return `"Exact"` when
  members share an exact byte hash, `"Very Similar"` when the max pairwise
  perceptual distance is `<= threshold // 2`, and `"Similar"` otherwise (up to
  `threshold`); verify with unit tests covering all three cases plus the exact
  midpoint boundary
- [ ] 1.2 Verify against the fixture set: `base.png` + `base_identical_copy.png`
  labeled `Exact`, `base.png` + `base_resized.png` labeled `Very Similar` at the
  default threshold; verify with a unit test

## 2. Update existing tests and docs

- [ ] 2.1 Update any existing tests/assertions in `tests/test_cli.py` and
  `tests/test_report.py` that reference the old numeric similarity score; verify
  the full test suite passes
- [ ] 2.2 Run `find-duplicates tests/fixtures/` and manually confirm the generated
  `duplicates.xlsx` shows category labels instead of numbers in the Similarity
  Score column

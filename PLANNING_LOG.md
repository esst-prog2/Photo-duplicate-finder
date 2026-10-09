# Planning Log

Append-only. Format: `YYYY-MM-DD | decision | decided by: User or Claude`

2026-09-23 | Keep an append-only planning log in PLANNING_LOG.md, with its rules in AGENTS.md | decided by: User
2026-09-23 | Log line format: date, decision and decider, separated by " | " | decided by: Claude
2026-09-23 | Use OpenSpec as the spec tool; version still open (1.13.0 was asked for, but the latest release is 1.11.0) | decided by: User
2026-09-23 | Correction: real package is @fission-ai/openspec on npm (the bare "openspec" package is unrelated/defunct); 1.13.0 exists and installs cleanly | decided by: Claude
2026-09-23 | Installed OpenSpec 1.13.0 globally via npm and ran `openspec init --tools claude` in this repo | decided by: User
2026-09-23 | Redid OpenSpec init without AI-tool integration: ran `openspec init --tools none`, keeping only openspec/config.yaml (untouched), openspec/specs/ (source of truth), openspec/changes/ (work in progress); removed .claude/ | decided by: User
2026-09-23 | Wrote OpenSpec change `build-mvp` (proposal, specs, design, tasks) for the MVP: Python + Pillow/imagehash/click/pytest, SHA-256 exact-hash + ahash near-dup detection, union-find grouping, CSV report; 4 capabilities: photo-scanning, exact-duplicate-detection, near-duplicate-detection, duplicate-report | decided by: User
2026-09-23 | Empty/no-matching-images folder is not an error: scan completes empty, pipeline reports zero duplicate groups; added scenario to photo-scanning spec and task 7.2 to build-mvp | decided by: User
2026-09-23 | Implemented and completed all build-mvp tasks (1.1-7.2): find_duplicates/{scanner,hashing,grouping,report,cli}.py, 23 passing tests; `duplicates.csv` is written next to (sibling of) the scanned folder, per README | decided by: User
2026-09-23 | Archived OpenSpec change build-mvp; its 4 capability specs (photo-scanning, exact-duplicate-detection, near-duplicate-detection, duplicate-report) are now the source of truth under openspec/specs/ | decided by: User
2026-09-23 | Wrote OpenSpec change `xlsx-report`: replace duplicates.csv with duplicates.xlsx (openpyxl) -- one stacked table per group (File, Similarity Score), blank-row separated, keep-file row highlighted; BREAKING change to duplicate-report capability | decided by: User
2026-09-23 | Implemented and archived xlsx-report; duplicate-report capability's "Write an Excel report" requirement is now the source of truth under openspec/specs/. Fixed a stale "CSV file" mention left in the capability's Purpose line, since archive doesn't rewrite Purpose from a delta | decided by: User
2026-09-23 | Cropped/edited photos are not detected as near-duplicates -- expected per README's explicit non-goal (rotated/cropped/heavily-edited duplicate detection), since average_hash isn't robust to cropping; left as a documented limitation, not fixed | decided by: User
2026-09-23 | Wrote OpenSpec change `similarity-categories`: replace raw Hamming-distance score with Exact/Very Similar/Similar labels; Exact = shared byte hash, Very Similar = distance <= threshold // 2, Similar = distance in (threshold // 2, threshold] | decided by: User
2026-09-23 | Implemented and archived similarity-categories. Fixed a bug found during manual verification: a mixed exact+near-duplicate group was labeled "Exact" if ANY pair shared an exact hash; now requires ALL members share the same exact hash | decided by: User
2026-09-23 | duplicates.xlsx silently overwrote an existing file with the same name -- discovered by testing. Wrote OpenSpec change `timestamped-report`: filename becomes duplicates_<YYYYMMDD>_<HHMM>.xlsx (minute precision, local time), and the CLI warns + prompts for confirmation before overwriting if that exact filename already exists | decided by: User
2026-09-23 | Implemented and archived timestamped-report; duplicate-report capability's spec now documents the timestamped filename and the overwrite-confirmation requirement as source of truth | decided by: User
2026-10-01 | Spike: For me the answer was already determined: A thirteen-row table plus one sentence: the widest safe threshold, the size of the largest group there, and how many groups contain a photo that does not belong. | decided by: User
2026-10-01 | Spike answer: widest safe threshold is 1 (largest group there has 9 elements, 32 groups total, 8 of them contain a photo that does not belong); feedback from last week is validated, the bridge/chaining problem needs to be addressed, and real photos need to be added to the hashing test process | decided by: User

| threshold | group_count | largest_group_size |
|-----------|-------------|---------------------|
| 0         | 22          | 2                   |
| 1         | 32          | 9                   |
| 2         | 25          | 43                  |
| 3         | 27          | 74                  |
| 4         | 26          | 96                  |
| 5         | 27          | 109                 |
| 6         | 30          | 125                 |
| 7         | 32          | 140                 |
| 8         | 36          | 153                 |
| 9         | 38          | 171                 |
| 10        | 30          | 201                 |
| 11        | 28          | 234                 |
| 12        | 24          | 259                 |

2026-10-01 | Wrote OpenSpec change `bounded-near-duplicate-groups` to fix the chaining bug the spike confirmed: replace single-linkage (transitive closure/union-find) grouping with greedy complete-linkage (clique-bounded) grouping, so every reported group's max internal pairwise distance never exceeds the threshold; also adds real (non-synthetic) photo fixtures to validate the approach | decided by: User
2026-10-01 | Implemented bounded-near-duplicate-groups: grouping.py's union-find replaced by cluster_by_threshold() (clique-bounded); find_near_duplicate_pairs removed as dead code once cli.py no longer used the old single-linkage pipeline; synthetic PNG fixtures replaced in place with real user-supplied JPEGs (base/base_identical_copy/base_resized/unrelated) rather than added alongside them; 36 tests passing including a chain regression test proving A and D never land in the same group | decided by: User
2026-10-01 | Archived bounded-near-duplicate-groups; near-duplicate-detection and duplicate-report specs now document the clique-bounded (all-pairs-within-threshold) grouping guarantee as source of truth | decided by: User
2026-10-03 | Default near-duplicate threshold changed from 5 to 1 (matches the spike's "widest safe threshold" of 1); specs only say "a documented default" so no spec change needed | decided by: User
2026-10-03 | Perceptual hash algorithm changed from average_hash (ahash) to phash, because ahash still grouped photos that only shared a vague colour scheme even at threshold 1; no spec change needed since the specs never name an algorithm, only "perceptual-hash Hamming distance" | decided by: User
2026-10-03 | Perceptual hash size set to 7 (49 bits), tried by hand on the user's own photos: size 16 and 10 were too strict even at higher thresholds, and 7 gave the best groups; sizes need not be powers of two, and the size is the PERCEPTUAL_HASH_SIZE constant in hashing.py | decided by: User
2026-10-03 | Default near-duplicate threshold changed from 1 to 8 (replaces the 5-to-1 line above), found by hand on the user's photos as the best value for phash at size 7; the spike's "widest safe threshold is 1" was measured on ahash and no longer applies | decided by: User
2026-10-09 | hw5 benchmark expected value, fixed before the program runs on this data: A test would go red if the feature does not categorizes the hand-picked test data right: 20 groups, each of size 4, and 0 contaminated groups. Source: planted data, not program output -- the user hand-picked 20 visually distinct photos (benchmark/sources/), and each will get 3 scripted copies (byte-identical, resized, re-saved at lower JPEG quality), so the expected counts follow from construction | decided by: User
2026-10-09 | Red then green for the hw5 benchmark test (the assignment requires showing both). The user required the demonstration; Claude chose the line: in find_duplicates/hashing.py, DEFAULT_NEAR_DUPLICATE_THRESHOLD changed from 8 to 40, then `pytest tests/test_benchmark.py -v --tb=short` went red (all 3 tests failed: 1 group of 80 photos instead of 20 groups of 4, and 1 contaminated group). The line was then put back to 8 (git diff empty) and the same command went green (3 passed). Both outputs follow | decided by: Claude

Red run (threshold 40, exit code 1):

```text
============================= test session starts =============================
platform win32 -- Python 3.11.15, pytest-9.1.1, pluggy-1.6.0 -- D:\Tanulas\MSC\AP\APClassProject\.venv\Scripts\python.exe
rootdir: D:\Tanulas\MSC\AP\APClassProject
configfile: pyproject.toml
collecting ... collected 3 items

tests/test_benchmark.py::test_benchmark_reports_the_expected_number_of_groups FAILED [ 33%]
tests/test_benchmark.py::test_benchmark_every_group_has_the_expected_size FAILED [ 66%]
tests/test_benchmark.py::test_benchmark_has_no_contaminated_groups FAILED [100%]

================================== FAILURES ===================================
____________ test_benchmark_reports_the_expected_number_of_groups _____________
tests\test_benchmark.py:57: in test_benchmark_reports_the_expected_number_of_groups
    assert len(reported_groups) == EXPECTED_GROUPS
E   AssertionError: assert 1 == 20
E    +  where 1 = len([['p01_identical.jpg', 'p01_orig.jpg', 'p01_recompressed.jpg', 'p01_resized.jpg', 'p02_identical.jpg', 'p02_orig.jpg', ...]])
______________ test_benchmark_every_group_has_the_expected_size _______________
tests\test_benchmark.py:63: in test_benchmark_every_group_has_the_expected_size
    assert sizes == [EXPECTED_GROUP_SIZE] * EXPECTED_GROUPS
E   AssertionError: assert [80] == [4, 4, 4, 4, 4, 4, ...]
E     
E     At index 0 diff: 80 != 4
E     Right contains 19 more items, first extra item: 4
E     
E     Full diff:
E       [
E     -     4,...
E     
E     ...Full output truncated (23 lines hidden), use '-vv' to show
__________________ test_benchmark_has_no_contaminated_groups __________________
tests\test_benchmark.py:73: in test_benchmark_has_no_contaminated_groups
    assert len(contaminated) == EXPECTED_CONTAMINATED_GROUPS, contaminated
E   AssertionError: [['p01_identical.jpg', 'p01_orig.jpg', 'p01_recompressed.jpg', 'p01_resized.jpg', 'p02_identical.jpg', 'p02_orig.jpg', ...]]
E   assert 1 == 0
E    +  where 1 = len([['p01_identical.jpg', 'p01_orig.jpg', 'p01_recompressed.jpg', 'p01_resized.jpg', 'p02_identical.jpg', 'p02_orig.jpg', ...]])
=========================== short test summary info ===========================
FAILED tests/test_benchmark.py::test_benchmark_reports_the_expected_number_of_groups
FAILED tests/test_benchmark.py::test_benchmark_every_group_has_the_expected_size
FAILED tests/test_benchmark.py::test_benchmark_has_no_contaminated_groups - A...
============================== 3 failed in 1.44s ==============================
```

Green run (threshold 8, exit code 0):

```text
============================= test session starts =============================
platform win32 -- Python 3.11.15, pytest-9.1.1, pluggy-1.6.0 -- D:\Tanulas\MSC\AP\APClassProject\.venv\Scripts\python.exe
rootdir: D:\Tanulas\MSC\AP\APClassProject
configfile: pyproject.toml
collecting ... collected 3 items

tests/test_benchmark.py::test_benchmark_reports_the_expected_number_of_groups PASSED [ 33%]
tests/test_benchmark.py::test_benchmark_every_group_has_the_expected_size PASSED [ 66%]
tests/test_benchmark.py::test_benchmark_has_no_contaminated_groups PASSED [100%]

============================== 3 passed in 1.17s ==============================
```

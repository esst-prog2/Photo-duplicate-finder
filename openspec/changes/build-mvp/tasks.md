## 1. Project setup

- [x] 1.1 Create `find_duplicates/` package and `tests/` directory; add `pyproject.toml`
  (or `setup.cfg`) declaring dependencies (Pillow, imagehash, click) and dev
  dependency (pytest); verify `pip install -e .` succeeds
- [x] 1.2 Add `tests/fixtures/` with synthetic, non-personal test images: a base
  image, a byte-identical copy, a resized copy of the base, and an unrelated image;
  verify the four files load correctly with Pillow in a throwaway script

## 2. Photo scanning (specs/photo-scanning)

- [x] 2.1 Implement `scanner.py`: list `.jpg`/`.png` files in a given folder,
  non-recursive; verify with a unit test that files in a subfolder are excluded
- [x] 2.2 Implement invalid-path handling (missing path, path is a file) with a
  clear error; verify with unit tests for both cases

## 3. Exact-duplicate detection (specs/exact-duplicate-detection)

- [x] 3.1 Implement `hashing.py` exact-hash function (SHA-256 over file bytes);
  verify with a unit test that the identical-copy fixture hashes equal to the base
  image and the unrelated fixture hashes different
- [x] 3.2 Implement exact-duplicate grouping (group files sharing a hash); verify
  with a unit test using the fixture set

## 4. Near-duplicate detection (specs/near-duplicate-detection)

- [x] 4.1 Implement `hashing.py` perceptual-hash function (`imagehash.average_hash`)
  and a Hamming-distance comparison; verify with a unit test comparing the base
  image against itself (distance 0)
- [x] 4.2 Add configurable similarity threshold (CLI `--threshold` option with a
  documented default); verify with a unit test that a custom threshold changes the
  match decision for a borderline case
- [x] 4.3 Verify against the required acceptance case: the resized-copy fixture is
  detected as a near-duplicate of the base image at the default threshold, and the
  unrelated fixture is not — as an explicit automated test (not just manual
  inspection)
- [x] 4.4 Exclude file pairs already grouped as exact duplicates from the
  near-duplicate comparison; verify with a unit test

## 5. Grouping and reporting (specs/duplicate-report)

- [x] 5.1 Implement `grouping.py` union-find merge of exact- and near-duplicate
  matches into single groups; verify with a unit test that a transitive match
  (A=B exact, B≈C near) produces one group of three, not two groups
- [x] 5.2 Implement `report.py` keep-candidate selection (largest file size, tie
  broken by resolution); verify with a unit test using fixtures of different sizes
- [x] 5.3 Implement CSV writer producing `duplicates.csv` (group members, similarity
  score, keep suggestion), including the no-duplicates-found case (file still
  created, no group rows); verify with unit tests for both cases

## 6. CLI wiring

- [x] 6.1 Implement `cli.py` orchestrating scan → hash → group → report, printing
  the one-line summary count; verify by running `find-duplicates tests/fixtures/`
  and checking the printed summary and generated `duplicates.csv` by hand
- [x] 6.2 Wire the console-script entry point in `pyproject.toml`; verify the
  `find-duplicates` command is available after `pip install -e .`

## 7. End-to-end verification

- [x] 7.1 Run the full test suite (`pytest`) and confirm all tests pass, including
  the three explicit cases from README.md section 4: identical files grouped,
  unrelated files not grouped, resized copy grouped as near-duplicate
- [x] 7.2 Add and verify a test for an empty/no-matching-images folder: running the
  CLI against it exits without error, writes `duplicates.csv` with no group rows,
  and prints a summary of zero exact duplicates and zero near-duplicate groups

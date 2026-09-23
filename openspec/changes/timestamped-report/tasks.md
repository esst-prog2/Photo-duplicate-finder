## 1. Timestamped filename

- [ ] 1.1 In `cli.py`, build the output path as
  `duplicates_<YYYYMMDD>_<HHMM>.xlsx` (local time, minute precision) instead of the
  fixed `duplicates.xlsx`; verify with a unit test that the generated filename
  matches the expected pattern
- [ ] 1.2 Run `find-duplicates tests/fixtures/` and confirm the report file is
  created with a timestamped name next to the folder

## 2. Overwrite confirmation

- [ ] 2.1 Before writing, check whether a file already exists at the computed
  output path; if so, warn and prompt for confirmation via `click.confirm(...,
  abort=True)` before overwriting; verify with a unit test (using `CliRunner`'s
  `input=` parameter) that declining aborts without writing and confirming
  proceeds with the overwrite
- [ ] 2.2 Verify with a unit test that no prompt appears when the target filename
  does not already exist

## 3. Update existing tests and docs

- [ ] 3.1 Update `tests/test_cli.py` assertions that assume the fixed
  `duplicates.xlsx` filename to work with the new timestamped name; verify the
  full test suite passes
- [ ] 3.2 Update `README.md`'s demo description to reflect the timestamped
  filename instead of the fixed `duplicates.xlsx`

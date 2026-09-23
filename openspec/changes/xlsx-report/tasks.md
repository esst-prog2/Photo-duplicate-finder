## 1. Dependency and report writer

- [ ] 1.1 Add `openpyxl` to `pyproject.toml` runtime dependencies and reinstall;
  verify `import openpyxl` succeeds in the project venv
- [ ] 1.2 Rewrite `write_report()` in `report.py` to build an `.xlsx` workbook:
  one stacked table per group (header row + one row per member), one blank row
  between groups, keep-file row highlighted with a fill color; verify with a unit
  test that opens the generated workbook and checks cell values, row highlighting,
  and the blank-row spacing between two groups
- [ ] 1.3 Verify the no-duplicates case still produces a valid, openable workbook
  with no group tables; verify with a unit test

## 2. Wiring and existing tests

- [ ] 2.1 Update `cli.py` to write `duplicates.xlsx` instead of `duplicates.csv`;
  verify by running `find-duplicates tests/fixtures/` and confirming
  `duplicates.xlsx` is created next to the folder with the expected group table
- [ ] 2.2 Update `tests/test_report.py` and `tests/test_cli.py` to assert against
  the new `.xlsx` output instead of CSV rows; verify the full test suite passes
- [ ] 2.3 Update `README.md`'s demo description from `duplicates.csv` to
  `duplicates.xlsx`; verify by re-reading section 1 for consistency with the new
  behavior

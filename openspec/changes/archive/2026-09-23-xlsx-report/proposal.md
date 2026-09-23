## Why

The current `duplicates.csv` output is a single flat table (one row per group,
member filenames joined with `;` in one cell), which is hard for a person to read:
groups aren't visually separated, and there's no way to highlight the suggested
"keep" file. Since the report is meant to be opened and reviewed by a person (per
README's demo), a per-group table layout in Excel with the keep row highlighted is
much more usable.

## What Changes

- **BREAKING**: Replace the CSV report with an Excel (`.xlsx`) report. The system no
  longer writes `duplicates.csv`.
- Each duplicate group is rendered as its own small table (File, Similarity Score
  columns) on a single sheet, with one blank row separating consecutive tables.
- The row for the suggested "keep" file within each group's table is highlighted
  with a fill color.
- The no-duplicates-found case still produces a valid (near-empty) workbook rather
  than erroring.

## Capabilities

### Modified Capabilities
- `duplicate-report`: the "Write a CSV report" requirement is replaced by a
  requirement to write a formatted Excel report with per-group tables and a
  highlighted keep row.

## Impact

- New runtime dependency: `openpyxl`.
- `find_duplicates/report.py`: `write_report()` changes from a CSV writer to an
  Excel writer; output filename changes from `duplicates.csv` to `duplicates.xlsx`.
- `find_duplicates/cli.py`: update the output path it passes to `write_report()`.
- `tests/test_report.py`, `tests/test_cli.py`: update to assert against the new
  `.xlsx` structure instead of CSV rows.
- `README.md`: update the demo description ("writes `duplicates.csv`" →
  "writes `duplicates.xlsx`").

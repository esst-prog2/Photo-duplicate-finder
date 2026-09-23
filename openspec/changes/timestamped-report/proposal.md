## Why

The report is currently always written to the fixed filename `duplicates.xlsx`, so
running the tool again on the same folder silently overwrites any earlier report —
including one a person may have manually annotated (e.g. marking which duplicates
they already deleted) — with no warning.

## What Changes

- The report filename includes a timestamp (date and time down to the minute), so
  consecutive runs produce distinct files instead of colliding by default.
- If the resulting filename happens to already exist (e.g. two runs within the same
  minute), the system warns the user and asks for confirmation before overwriting;
  declining aborts without writing the report.

## Capabilities

### Modified Capabilities
- `duplicate-report`: the "Write an Excel report" requirement's filename changes
  from the fixed `duplicates.xlsx` to a timestamped name, and gains an
  overwrite-confirmation requirement for the rare collision case.

## Impact

- `find_duplicates/cli.py`: build the timestamped output filename and add an
  overwrite confirmation prompt before calling `write_report()`.
- `tests/test_cli.py`: update assertions that currently look for a fixed
  `duplicates.xlsx` filename; add tests for the collision/confirmation path.
- `README.md`: update the demo description of the output filename.

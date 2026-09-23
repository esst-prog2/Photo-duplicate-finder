## Context

See proposal.md for motivation. This covers where the timestamp comes from, its
exact format, and how the overwrite-confirmation prompt fits into `cli.py`'s
`main()`.

## Goals / Non-Goals

**Goals:**
- Make consecutive runs against the same folder produce distinct report files by
  default.
- Never silently destroy an existing report file (or anything else) at the target
  path without the user's explicit go-ahead.

**Non-Goals:**
- A full history/versioning system for reports (e.g. keeping N old reports) — a
  timestamp in the filename is enough for this MVP; no cleanup logic is added.
- Changing where the report is written (still next to the scanned folder, per the
  existing `duplicate-report` behavior) — only the filename and the
  exists-check change.

## Decisions

**Timestamp format: `duplicates_%Y%m%d_%H%M.xlsx` (minute precision).**
Rationale: sortable by filename, human-readable, and minute precision is enough to
distinguish separate runs in normal use (a person re-running the tool seconds apart
is the only realistic collision case, which is exactly what the overwrite-confirm
requirement exists to handle). Using `datetime.now()` (local time, matching what a
person doing a manual demo would expect to see) rather than UTC.

**Confirmation via `click.confirm()`.**
Rationale: `click` is already a dependency and provides a ready-made y/n prompt with
sane default handling; no need for a custom input loop. `click.confirm(..., abort=True)`
raises `click.Abort`, which exits the program without writing the report — matching
the "abort without writing" requirement directly.

**Where the check happens:** in `cli.py`'s `main()`, right before calling
`write_report()` — build the timestamped path, check `Path.exists()`, prompt if so,
then proceed. `report.py`'s `write_report()` itself is unchanged; it still just
takes a path and writes to it unconditionally. Keeping the confirmation in `cli.py`
(rather than inside `write_report()`) matches the existing separation: `report.py`
is a pure writer, `cli.py` owns user-facing interaction (it already owns the error
message for `ScanTargetError`).

**Test approach for the prompt:** Click's `CliRunner.invoke()` supports an `input=`
parameter to simulate stdin for prompts, so the confirm/decline paths can be tested
the same way the existing CLI tests work, without real interactive input.

## Risks / Trade-offs

- **Prompting breaks fully non-interactive/scripted use** (e.g. a cron job) →
  Mitigation: this only prompts on the rare collision case (same-minute rerun);
  normal runs never hit it. Acceptable for a class project's interactive use case;
  not adding a `--yes`/`--force` flag to bypass it since no non-interactive use
  case has been requested.
- **Minute-precision collisions still possible** (two runs within the same minute)
  → Mitigation: exactly what the overwrite-confirmation requirement handles; not
  a bug, an expected and covered case.

## Open Questions

None.

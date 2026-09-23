## Context

See proposal.md for motivation. This covers how `write_report()` in
`find_duplicates/report.py` changes from a CSV writer to an Excel writer. The
`DuplicateGroup` dataclass (members, similarity_score, keep) it takes as input is
unchanged — only the output format changes.

## Goals / Non-Goals

**Goals:**
- Satisfy the modified `duplicate-report` spec: one table per group on a single
  sheet, blank-row separated, keep row highlighted.
- Keep `write_report()`'s signature and input shape (`list[DuplicateGroup]`,
  output path) the same, so callers (`cli.py`) barely change.

**Non-Goals:**
- Multiple sheets, charts, or other Excel features beyond simple tables and a fill
  color — not needed for MVP readability.
- Preserving CSV output alongside Excel (the proposal is an explicit replacement,
  not an addition).

## Decisions

**Library: `openpyxl`.**
Rationale: the standard, dependency-light way to write `.xlsx` with cell styling
(fill colors) from Python; no need for pandas' heavier dependency chain since we're
not doing data analysis, just writing formatted rows.

**Layout algorithm: sequential row cursor.**
Write groups top-to-bottom on one worksheet. For each group: write a 2-column
header row (`File`, `Similarity Score`), then one row per member (filename,
similarity score repeated per row — the score is a group-level value), applying a
fill color to the row whose filename matches `group.keep`. Advance the row cursor
by 1 (blank row) between groups. This is simpler than a grid/2D layout and matches
the proposal's "tables next to/under each other" as stacked (under each other),
which reads naturally top-to-bottom in Excel.
Alternative considered: side-by-side tables (columns instead of rows) — rejected
as harder to scroll through with many groups, and stacked tables need no column
math.

**Highlighting: `openpyxl.styles.PatternFill` solid fill on the keep row's cells.**
Rationale: simplest way to visually distinguish a row; applied to both cells in
that row (File, Similarity Score) so the whole row is highlighted, not just one
cell.

**No-duplicates case:** create and save a workbook with one (default) empty
worksheet — no headers, no tables. A person opening it sees a blank sheet, which
correctly communicates "nothing found" without needing special-case messaging.

**Module boundary:** stays in `report.py`; `choose_keep()` and `DuplicateGroup` are
unchanged, only `write_report()`'s body and the file extension it targets change.
`cli.py` changes only the output filename it constructs (`duplicates.xlsx` instead
of `duplicates.csv`).

## Risks / Trade-offs

- **Harder to consume programmatically than CSV** (per-group tables aren't one flat
  table) → Mitigation: explicitly accepted in the proposal; this report is for
  human review, not downstream tooling, per the project's own use case.
- **New dependency (`openpyxl`)** → Mitigation: it's a widely-used, pure-Python
  (no compiled extensions) library; acceptable weight for a class project.

## Open Questions

None.

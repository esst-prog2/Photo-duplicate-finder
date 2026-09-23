## RENAMED Requirements
- FROM: `### Requirement: Write a CSV report`
- TO: `### Requirement: Write an Excel report`

## MODIFIED Requirements

### Requirement: Write an Excel report
The system SHALL write a `duplicates.xlsx` file next to the scanned folder,
containing one table per duplicate group on a single worksheet. Each table SHALL
have a header row ("File", "Similarity Score") followed by one row per member file
in that group, and consecutive tables SHALL be separated by exactly one blank row.
Within each table, the row for the suggested "keep" file SHALL be visually
highlighted (fill color) to distinguish it from the other rows.

#### Scenario: Report written after a scan with duplicates
- **WHEN** the scan finds at least one exact or near-duplicate group
- **THEN** `duplicates.xlsx` is created next to the scanned folder with one table
  per group, each table's keep-file row highlighted, and one blank row between
  consecutive tables

#### Scenario: Report written after a scan with no duplicates
- **WHEN** the scan finds no exact or near-duplicate groups
- **THEN** `duplicates.xlsx` is still created, as a valid workbook containing no
  group tables

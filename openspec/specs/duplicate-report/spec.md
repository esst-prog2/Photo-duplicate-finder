# duplicate-report Specification

## Purpose
Turns the exact- and near-duplicate matches into a single, actionable report: one
group per set of duplicates, a suggested file to keep, an Excel file, and a printed
summary.

## Requirements

### Requirement: Merge exact and near-duplicate matches into groups
The system SHALL combine exact-duplicate and near-duplicate matches that share a
file into a single group, so no file appears in more than one output group.

#### Scenario: A group spans both exact and near duplicates
- **WHEN** file A and file B are exact duplicates, and file B and file C are
  near-duplicates
- **THEN** files A, B, and C are reported as one group, not two

### Requirement: Suggest a file to keep per group
The system SHALL suggest exactly one file to keep per duplicate group, choosing the
file with the largest file size or highest resolution in that group.

#### Scenario: Group with files of different sizes
- **WHEN** a duplicate group contains files of different sizes or resolutions
- **THEN** the largest / highest-resolution file is marked "keep" and the rest are
  marked "duplicate"

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

### Requirement: Print a summary count
The system SHALL print a one-line summary after scanning, stating the number of
exact duplicates found and the number of near-duplicate groups found.

#### Scenario: Summary reflects scan results
- **WHEN** a scan completes
- **THEN** the system prints a summary line with the exact-duplicate count and the
  near-duplicate group count from that scan

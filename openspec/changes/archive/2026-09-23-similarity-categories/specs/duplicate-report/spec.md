## MODIFIED Requirements

### Requirement: Write an Excel report
The system SHALL write a `duplicates.xlsx` file next to the scanned folder,
containing one table per duplicate group on a single worksheet. Each table SHALL
have a header row ("File", "Similarity Score") followed by one row per member file
in that group, and consecutive tables SHALL be separated by exactly one blank row.
Within each table, the row for the suggested "keep" file SHALL be visually
highlighted (fill color) to distinguish it from the other rows.

The "Similarity Score" column SHALL show one of three category labels for the
group, not a raw distance number:
- `Exact`, when the group's members share an exact byte hash.
- `Very Similar`, when the group's members do not share an exact byte hash, and
  their perceptual-hash Hamming distance is less than or equal to half of the
  configured near-duplicate threshold (rounded down).
- `Similar`, when the group's members do not share an exact byte hash, and their
  perceptual-hash Hamming distance is above half of the configured threshold but
  within the threshold.

#### Scenario: Report written after a scan with duplicates
- **WHEN** the scan finds at least one exact or near-duplicate group
- **THEN** `duplicates.xlsx` is created next to the scanned folder with one table
  per group, each table's keep-file row highlighted, and one blank row between
  consecutive tables

#### Scenario: Report written after a scan with no duplicates
- **WHEN** the scan finds no exact or near-duplicate groups
- **THEN** `duplicates.xlsx` is still created, as a valid workbook containing no
  group tables

#### Scenario: Exact-duplicate group is labeled Exact
- **WHEN** a duplicate group's members share an exact byte hash
- **THEN** the group's Similarity Score column shows `Exact`

#### Scenario: Near-duplicate group within the lower half of the threshold is labeled Very Similar
- **WHEN** a duplicate group's members do not share an exact byte hash, and their
  perceptual-hash Hamming distance is at or below half of the configured threshold
- **THEN** the group's Similarity Score column shows `Very Similar`

#### Scenario: Near-duplicate group in the upper half of the threshold is labeled Similar
- **WHEN** a duplicate group's members do not share an exact byte hash, and their
  perceptual-hash Hamming distance is above half of the configured threshold but
  within the threshold
- **THEN** the group's Similarity Score column shows `Similar`

# duplicate-report Specification

## Purpose
Turns the exact- and near-duplicate matches into a single, actionable report: one
group per set of duplicates, a suggested file to keep, an Excel file, and a printed
summary.

## Requirements

### Requirement: Merge exact and near-duplicate matches into groups
The system SHALL combine exact-duplicate and near-duplicate matches into groups
such that every pair of members within a group is either an exact duplicate of
each other or within the configured near-duplicate threshold of each other, so no
file appears in more than one output group, and no
group is formed purely by chaining through intermediate files that are not
themselves mutually similar.

#### Scenario: A group spans both exact and near duplicates
- **WHEN** file A and file B are exact duplicates, and file B and file C are
  near-duplicates (within the threshold of B)
- **THEN** files A, B, and C are reported as one group, not two

#### Scenario: A chain whose ends are not similar is not merged into one group
- **WHEN** files A, B, C, and D form a chain of pairwise near-duplicate matches
  (A-B, B-C, C-D each within the threshold), but A and D are not within the
  threshold of each other
- **THEN** A and D are not reported in the same group

### Requirement: Suggest a file to keep per group
The system SHALL suggest exactly one file to keep per duplicate group: the file with
the largest file size, and when several files tie on file size, the one with the
highest resolution (width times height). The report marks the suggested file only
by highlighting its row; the other rows are left unmarked.

#### Scenario: Group with files of different file sizes
- **WHEN** a duplicate group contains files of different file sizes
- **THEN** the largest file is the suggested keep file, even if another file in the
  group has a higher resolution

#### Scenario: Group whose files have the same file size
- **WHEN** a duplicate group contains files of equal file size but different
  resolutions
- **THEN** the highest-resolution file is the suggested keep file

### Requirement: Write an Excel report
The system SHALL write a `duplicates_<YYYYMMDD>_<HHMM>.xlsx` file (the date and
time the scan ran, to the minute) next to the scanned folder, that is, in the parent
directory of the scanned folder. The folder is resolved to an absolute path first,
so a folder given as `.` also gets its report in its parent directory. The workbook
SHALL contain one table per duplicate group on a single worksheet. Each table SHALL
have a header row ("File", "Similarity") followed by one row per member file
in that group, and consecutive tables SHALL be separated by exactly one blank row.
Within each table, the row for the suggested "keep" file SHALL be visually
highlighted (fill color) to distinguish it from the other rows.

#### Scenario: Report written after a scan with duplicates
- **WHEN** the scan finds at least one exact or near-duplicate group
- **THEN** a `duplicates_<YYYYMMDD>_<HHMM>.xlsx` file is created next to the
  scanned folder with one table per group, each table's keep-file row highlighted,
  and one blank row between consecutive tables

#### Scenario: Report written after a scan with no duplicates
- **WHEN** the scan finds no exact or near-duplicate groups
- **THEN** a `duplicates_<YYYYMMDD>_<HHMM>.xlsx` file is still created, as a valid
  workbook containing no group tables

#### Scenario: Folder given as the current directory
- **WHEN** the user runs the CLI with `.` as the folder
- **THEN** the report is created in the parent directory of the current directory,
  not inside the scanned folder

### Requirement: Label each group with a similarity category
The "Similarity" column SHALL show one of three category labels for the
group, not a raw distance number:
- `Exact`, when all of the group's members share one exact byte hash.
- `Very Similar`, when the group's members do not all share one exact byte hash,
  and the largest perceptual-hash Hamming distance between any two of its members
  is less than or equal to half of the configured near-duplicate threshold
  (rounded down).
- `Similar`, when the group's members do not all share one exact byte hash, and
  that largest pairwise distance is above half of the configured threshold but
  within the threshold.

#### Scenario: Exact-duplicate group is labeled Exact
- **WHEN** all of a duplicate group's members share one exact byte hash
- **THEN** the group's Similarity column shows `Exact`

#### Scenario: A group that mixes exact duplicates with a merely similar file is not Exact
- **WHEN** a duplicate group contains two byte-identical files and a third file
  that is only perceptually similar
- **THEN** the group's Similarity column does not show `Exact`; it shows
  `Very Similar` or `Similar` according to the largest pairwise distance

#### Scenario: Near-duplicate group within the lower half of the threshold is labeled Very Similar
- **WHEN** a duplicate group's members do not all share one exact byte hash, and
  the largest perceptual-hash Hamming distance between any two of them is at or
  below half of the configured threshold
- **THEN** the group's Similarity column shows `Very Similar`

#### Scenario: Near-duplicate group in the upper half of the threshold is labeled Similar
- **WHEN** a duplicate group's members do not all share one exact byte hash, and
  the largest perceptual-hash Hamming distance between any two of them is above
  half of the configured threshold but within the threshold
- **THEN** the group's Similarity column shows `Similar`

### Requirement: Print a summary count
The system SHALL print a one-line summary after scanning, stating the number of
exact duplicates found and the number of near-duplicate groups found. "Exact
duplicates found" is the number of sets of two or more byte-identical files,
counted independently of the threshold. "Near-duplicate groups found" is the number
of reported groups whose members are not all byte-identical. A reported group that
contains both a byte-identical pair and a merely similar file is counted in both
numbers, so the two numbers do not necessarily add up to the number of tables in
the report.

#### Scenario: Summary reflects scan results
- **WHEN** a scan completes
- **THEN** the system prints a summary line with the exact-duplicate count and the
  near-duplicate group count from that scan

#### Scenario: One group that is counted in both numbers
- **WHEN** the folder holds a photo, a byte-identical copy of it, and a resized
  copy of it
- **THEN** the summary reads "1 exact duplicates found, 1 near-duplicate groups
  found." while the report contains a single table

### Requirement: Warn before overwriting an existing report file
The system SHALL check, before writing the report, whether a file already exists at
the timestamped output path. If one exists, the system SHALL warn the user and ask
for confirmation before overwriting it. If the user declines, the system SHALL
abort without writing the report and without producing a partial or corrupted file.
An empty answer (just pressing Enter) SHALL count as declining.

#### Scenario: Target filename does not exist
- **WHEN** no file exists at the timestamped output path
- **THEN** the system writes the report without prompting

#### Scenario: Target filename already exists and the user confirms
- **WHEN** a file already exists at the timestamped output path, and the user
  confirms the overwrite prompt
- **THEN** the system overwrites the existing file with the new report

#### Scenario: Target filename already exists and the user declines
- **WHEN** a file already exists at the timestamped output path, and the user
  declines the overwrite prompt
- **THEN** the system exits without writing the report, and the existing file is
  left unchanged

#### Scenario: The user presses Enter without answering
- **WHEN** a file already exists at the timestamped output path, and the user
  presses Enter at the overwrite prompt without typing an answer
- **THEN** the system treats it as declining: it exits without writing the report,
  and the existing file is left unchanged

## Purpose

Identifies files that are byte-for-byte identical, so they can be reported with
certainty and excluded from the more error-prone near-duplicate comparison.

## ADDED Requirements

### Requirement: Detect byte-identical files
The system SHALL group two or more scanned files as exact duplicates when their
file contents are identical, regardless of filename.

#### Scenario: Two identical files
- **WHEN** the scanned folder contains two files with identical byte content
- **THEN** the system groups them together as an exact-duplicate group

#### Scenario: Two unrelated files
- **WHEN** the scanned folder contains two files with different byte content
- **THEN** the system does not group them as exact duplicates

### Requirement: Exact duplicates are excluded from near-duplicate comparison
The system SHALL NOT run the near-duplicate comparison between two files that have
already been grouped as exact duplicates of each other.

#### Scenario: File already matched as an exact duplicate
- **WHEN** two files have been grouped as exact duplicates
- **THEN** those two files are not also compared against each other in the
  near-duplicate pass

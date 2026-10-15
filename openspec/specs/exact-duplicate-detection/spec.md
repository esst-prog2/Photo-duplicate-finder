# exact-duplicate-detection Specification

## Purpose
Identifies files that are byte-for-byte identical, so they can be reported with
certainty, labelled as exact, and counted separately from near-duplicates.

## Requirements

### Requirement: Detect byte-identical files
The system SHALL group two or more scanned files as exact duplicates when their
file contents are identical, regardless of filename. Byte-identical files SHALL
always be reported in the same group.

#### Scenario: Two identical files
- **WHEN** the scanned folder contains two files with identical byte content
- **THEN** the system groups them together as an exact-duplicate group

#### Scenario: Two unrelated files
- **WHEN** the scanned folder contains two files with different byte content
- **THEN** the system does not group them as exact duplicates

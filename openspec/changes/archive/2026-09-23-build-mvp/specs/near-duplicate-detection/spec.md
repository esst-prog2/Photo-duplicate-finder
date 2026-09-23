## Purpose

Identifies files that are visually similar but not byte-identical (e.g. a resized or
re-compressed copy of the same photo), using a perceptual similarity measure and a
configurable threshold.

## ADDED Requirements

### Requirement: Detect visually similar files within a threshold
The system SHALL compute a perceptual similarity score between two files and SHALL
group them as near-duplicates when that score is within a configurable threshold.

#### Scenario: A photo and a resized copy of it
- **WHEN** the scanned folder contains a photo and a resized (but otherwise
  unmodified) copy of that photo
- **THEN** the system groups them together as a near-duplicate group

#### Scenario: Two unrelated photos
- **WHEN** the scanned folder contains two unrelated photos
- **THEN** the system does not group them as near-duplicates

### Requirement: Similarity threshold is configurable
The system SHALL allow the user to configure the similarity threshold used for
near-duplicate detection, with a sensible default when none is given.

#### Scenario: User supplies a custom threshold
- **WHEN** the user runs the CLI with a custom similarity threshold
- **THEN** the system uses that threshold instead of the default when deciding
  whether two files are near-duplicates

#### Scenario: User supplies no threshold
- **WHEN** the user runs the CLI without specifying a threshold
- **THEN** the system uses its documented default threshold

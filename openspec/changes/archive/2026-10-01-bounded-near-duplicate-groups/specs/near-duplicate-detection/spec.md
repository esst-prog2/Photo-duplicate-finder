## MODIFIED Requirements

### Requirement: Detect visually similar files within a threshold
The system SHALL compute a perceptual similarity score between two files and SHALL
group them as near-duplicates when that score is within a configurable threshold.
When more than two files are grouped together, the system SHALL require every pair
of members in that group to be within the threshold of each other — a chain of
pairwise matches alone (where some pair in the group exceeds the threshold) SHALL
NOT be sufficient to form or extend a group.

#### Scenario: A photo and a resized copy of it
- **WHEN** the scanned folder contains a photo and a resized (but otherwise
  unmodified) copy of that photo
- **THEN** the system groups them together as a near-duplicate group

#### Scenario: Two unrelated photos
- **WHEN** the scanned folder contains two unrelated photos
- **THEN** the system does not group them as near-duplicates

#### Scenario: A chain of pairwise matches whose ends are not themselves similar
- **WHEN** the scanned folder contains photos A, B, C, and D, where A-B, B-C, and
  C-D are each within the threshold of each other, but A and D are not within the
  threshold of each other
- **THEN** the system does not place A and D in the same group; A and D are split
  into separate groups (or smaller groups that each satisfy the all-pairs-within-
  threshold requirement)

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

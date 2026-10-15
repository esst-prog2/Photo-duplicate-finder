# near-duplicate-detection Specification

## Purpose
Identifies files that are visually similar but not byte-identical (e.g. a resized or
re-compressed copy of the same photo), using a perceptual similarity measure and a
configurable threshold.

## Requirements

### Requirement: Detect visually similar files within a threshold
The system SHALL compute a perceptual distance between two files (the Hamming
distance between their perceptual hashes; the smaller it is, the more alike the
files look), and two files whose distance is within a configurable threshold are
eligible to be grouped as near-duplicates. Photos are compared the way they are
displayed: the system SHALL apply a photo's EXIF orientation tag before comparing,
so the same picture stored upright or stored turned with an orientation tag looks
the same. The system SHALL only report a group of more than two files when
every pair of its members is within the threshold of each other — a chain of
pairwise matches alone (where some pair in the group exceeds the threshold) SHALL
NOT be sufficient to form or extend a group. Being within the threshold of another
file does not by itself guarantee being grouped with it: a file that is within the
threshold of two files that are not within the threshold of each other SHALL be
placed with at most one of them.

#### Scenario: A photo and a resized copy of it
- **WHEN** the scanned folder contains a photo and a resized (but otherwise
  unmodified) copy of that photo
- **THEN** the system groups them together as a near-duplicate group

#### Scenario: A copy stored turned, with an EXIF orientation tag
- **WHEN** the scanned folder contains a photo and a copy of it whose pixels are
  turned 90 degrees and whose EXIF orientation tag turns them back when displayed
- **THEN** the system compares the two as displayed and they are within the
  threshold of each other

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

#### Scenario: A file within the threshold of two files that are not similar to each other
- **WHEN** photos A, B, and C are such that A-B and A-C are each within the
  threshold, but B and C are not within the threshold of each other
- **THEN** A is grouped with at most one of B and C, and B and C are never in the
  same group

### Requirement: Similarity threshold is configurable
The system SHALL allow the user to configure the similarity threshold used for
near-duplicate detection, with a sensible default when none is given. The threshold
SHALL be a whole number of zero or more; a negative threshold SHALL be rejected.

#### Scenario: User supplies a custom threshold
- **WHEN** the user runs the CLI with a custom similarity threshold
- **THEN** the system uses that threshold instead of the default when deciding
  whether two files are near-duplicates

#### Scenario: User supplies no threshold
- **WHEN** the user runs the CLI without specifying a threshold
- **THEN** the system uses its documented default threshold

#### Scenario: User supplies a negative threshold
- **WHEN** the user runs the CLI with a threshold below zero
- **THEN** the system rejects it with a usage error and exits without writing a
  report

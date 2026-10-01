## MODIFIED Requirements

### Requirement: Merge exact and near-duplicate matches into groups
The system SHALL combine exact-duplicate and near-duplicate matches into groups
such that every pair of members within a group is either an exact duplicate of
each other or within the configured near-duplicate threshold of each other (a
clique-bounded group), so no file appears in more than one output group, and no
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

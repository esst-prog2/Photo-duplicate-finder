## Context

See proposal.md for motivation, including the spike's empirical evidence
(`spike/threshold-spike-results.csv`): largest-group size grows from 2 at
threshold 0 to 259 at threshold 12 on ~300 real photos, and even the "widest safe"
threshold (1) still produced 8 contaminated groups out of 32. This covers how
`grouping.py` and `cli.py`'s `run()` change to eliminate the chaining, and how real
photographs get added to the test fixtures.

## Goals / Non-Goals

**Goals:**
- Guarantee that every reported group's maximum internal pairwise distance never
  exceeds the configured threshold, regardless of group size or chain length.
- Validate the near-duplicate detection approach (not just the grouping fix) against
  real photographs, not only synthetic test images.

**Non-Goals:**
- Finding the mathematically optimal clique cover (minimum number of maximal
  cliques). Clique cover is NP-hard in general; at this project's scale (low
  hundreds of files per README's existing scope) a greedy approach is fast enough
  and "every reported group is a valid clique" is the actual correctness property
  needed — optimality of the partition is not.
- Re-deciding the perceptual hash algorithm (`ahash`) or the default threshold value
  itself. Those are separate questions from the chaining bug; the real-photo
  fixtures are added to validate the existing approach, not to pick a new one.
  (The spike's own threshold recommendation is a separate, already-logged decision
  in PLANNING_LOG.md, not something this change overrides.)

## Decisions

**Grouping algorithm: greedy complete-linkage (clique-bounded) clustering.**
For each file not yet assigned to a group, start a new group containing it, then
scan the remaining unassigned files in order and add any file to the group only if
its distance to **every** current member of the group is within the threshold.
Repeat until all files are assigned. This guarantees every produced group is a
clique in the "within threshold" graph: by construction, no member was ever added
unless it matched every existing member.
Alternative considered: exact maximum clique cover — rejected as unnecessary
complexity (NP-hard, no benefit at this scale) per the Non-Goals above.
Alternative considered: keep single-linkage but post-hoc split any group whose
diameter exceeds the threshold — rejected because deciding *how* to split
correctly is exactly the same clique problem; building valid cliques from the start
is simpler than detecting and repairing invalid ones after the fact.

**Distance used for clustering: perceptual Hamming distance for every pair,
computed directly** (not the old `find_near_duplicate_pairs`, which pre-filtered to
only near-duplicate-threshold pairs excluding anything already exact-matched).
Rationale: exact-duplicate files are byte-identical, so their perceptual hashes are
identical too (distance 0) — they automatically satisfy "within threshold" against
anything a clique already contains, by the triangle inequality (Hamming distance is
a true metric: `distance(A, C) <= distance(A, B) + distance(B, C)`; if A and B are
byte-identical, distance(A, B) = 0, so distance(A, C) = distance(B, C)). This means
a single clustering pass over real perceptual distances naturally produces the
same "exact + near merge into one group" behavior the old code achieved with
separate exact-group and near-pair logic — no special-casing needed in the
clustering function itself.
`group_by_exact_hash` and `exact_hash` are still used, but only for: (a) the
"N exact duplicates found" summary count, and (b) the `Exact` similarity-score
label (which requires *all* group members to share one exact hash, per the
existing similarity-categories behavior) — not for the clustering decision itself.

**Where the logic lives:** `grouping.py` gains the new clustering function
(replacing `merge_duplicate_groups`'s union-find body, same module responsibility).
`cli.py`'s `run()` changes to: compute each file's perceptual hash once, pass the
hash map and threshold to the new clustering function, and keep using
`group_by_exact_hash` separately for the summary count and `_group_similarity_score`.

**Real-photo fixtures: a small number of genuinely photographic images, not a
personal library.**
Per README's existing privacy constraint (public domain or self-taken test photos,
not real personal photos), add 2-3 real photographs: one base photo, one real
resized/recompressed copy of it (e.g. actually saved at a different JPEG quality,
not just resized in-memory), and one unrelated real photo. These supplement, not
replace, the existing synthetic fixtures (the synthetic ones stay useful for fast,
exact boundary-condition tests; the real ones validate the approach actually works
on real camera output).
Source: images the user already has rights to use for this (self-taken or public
domain), supplied directly rather than fetched from an untrusted source.

## Risks / Trade-offs

- **Greedy clustering is order-dependent and not globally optimal** (a different
  iteration order could produce a different, also-valid partition into cliques) →
  Mitigation: explicitly accepted per the Non-Goals above; correctness (valid
  cliques) matters here, not which particular valid partition is chosen.
- **Group sizes/membership will differ from before for borderline chains** →
  Mitigation: this is the fix, not a regression; the old behavior was the bug the
  spike's data demonstrated.
- **O(n^2) worst case for the greedy scan** (checking a candidate against every
  current group member) → Mitigation: acceptable at the project's existing scale
  (low hundreds of files); same scale assumption the MVP design already made for
  pairwise near-duplicate comparison.

## Open Questions

None.

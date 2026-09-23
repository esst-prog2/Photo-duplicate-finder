## Context

See proposal.md for motivation. This covers how `_group_similarity_score()` in
`find_duplicates/cli.py` changes from returning a raw Hamming-distance string to a
category label, and how it decides which category applies.

## Goals / Non-Goals

**Goals:**
- Satisfy the modified `duplicate-report` spec: `Exact` / `Very Similar` /
  `Similar` labels instead of a raw number.
- Keep the cutoff between `Very Similar` and `Similar` tied to the actual
  `--threshold` used for that run, not a hardcoded constant.

**Non-Goals:**
- Changing how grouping or matching itself works — this only changes how an
  already-formed group's score is *labeled*, not which files end up in a group.
- A configurable cutoff (e.g. `--very-similar-threshold`) — the midpoint-of-threshold
  rule is fixed logic, not a new CLI option, to keep the surface area small.

## Decisions

**Exact check first, independent of distance.** A group is `Exact` if any two of
its members share an exact byte hash (reuse the same exact-hash equality already
computed for grouping) — checked before computing/considering perceptual distance
at all. This matches the current behavior where exact-duplicate members also score
a perceptual distance of 0, but makes the "these are literally the same bytes"
case explicit instead of indistinguishable from a very-close near-duplicate.

**Very Similar / Similar split: `threshold // 2` as the midpoint.**
Rationale: ties the boundary to whatever threshold the user actually configured,
so raising `--threshold` doesn't produce a "Similar" result outside what was agreed
in the last conversation (avoid a hardcoded cutoff that could exceed a custom
threshold). Integer floor division keeps it simple; at the default threshold of 5,
this gives Very Similar = distance 0-2, Similar = distance 3-5, matching what was
discussed.
Alternative considered: a fixed cutoff (e.g. always distance <= 2 is "Very
Similar") — rejected because it would misbehave for a much larger or smaller
`--threshold` (e.g. threshold=20 would call distance-3 "Similar" even though it's
still quite close relative to that threshold).

**Where the logic lives:** stays in `cli.py`'s `_group_similarity_score()`, since
it already has access to per-pair exact-hash and perceptual-distance information
computed during `run()`. `report.py` and `DuplicateGroup` are unchanged — the field
is still a plain string, just with different contents.

## Risks / Trade-offs

- **Losing the precise distance number** → Mitigation: explicitly the point of
  this change (per the "Why" in proposal.md) — the category is more useful to a
  non-technical reviewer than a raw bit-distance number.
- **Threshold-relative midpoint could feel arbitrary at unusual threshold values**
  (e.g. threshold=1 means Very Similar is only distance 0) → Mitigation: acceptable
  for MVP; not worth a separate configurable cutoff per the non-goals above.

## Open Questions

None.

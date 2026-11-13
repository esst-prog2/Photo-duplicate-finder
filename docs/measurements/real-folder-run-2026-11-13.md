# Real-folder run, 2026-11-13

A check of the tool on one folder of the owner's own photos. It is the source
for any "what it catches and misses" sentence on the promo page.

## Setup
- Folder: 414 pictures, the owner's own photos. The folder itself is not part of this record.
- Run on 2026-11-13 with the default threshold of 8.
- Ground truth: the owner compared the report with the original folder by hand.

## Result
| Measure | Value |
|---|---|
| Pictures in the folder | 414 |
| Pictures the tool put into groups | 89, in 41 groups |
| Wrong groups (unrelated pictures together) | 0 |
| Incomplete groups (a family split across groups) | 0 |
| Pictures with a look-alike the tool did not group | 30 |
| Those 30 as families | 14: 2 triplets and 12 twins |

## Reading it
- Families that had look-alikes: 41 found + 14 missed = 55. The tool found 41 of 55 families (about three quarters).
- Pictures that had a look-alike: 89 + 30 = 119. The tool grouped 89 of them (about three quarters).
- Every missed family was missed whole: no family was split, and no group mixed unrelated pictures.
- Not recorded: why each of the 14 families was missed (for example a crop, a turn or a border). The 30 pictures were not sorted by kind of change.

## Limits of this record
- One folder, one run, one person's own photos. It shows what happened here, not what any other folder will give.
- The per-picture lists are not saved, so the run cannot be repeated from this file alone.

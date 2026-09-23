# Planning Log

Append-only. Format: `YYYY-MM-DD | decision | decided by: User or Claude`

2026-09-23 | Keep an append-only planning log in PLANNING_LOG.md, with its rules in AGENTS.md | decided by: User
2026-09-23 | Log line format: date, decision and decider, separated by " | " | decided by: Claude
2026-09-23 | Use OpenSpec as the spec tool; version still open (1.13.0 was asked for, but the latest release is 1.11.0) | decided by: User
2026-09-23 | Correction: real package is @fission-ai/openspec on npm (the bare "openspec" package is unrelated/defunct); 1.13.0 exists and installs cleanly | decided by: Claude
2026-09-23 | Installed OpenSpec 1.13.0 globally via npm and ran `openspec init --tools claude` in this repo | decided by: User
2026-09-23 | Redid OpenSpec init without AI-tool integration: ran `openspec init --tools none`, keeping only openspec/config.yaml (untouched), openspec/specs/ (source of truth), openspec/changes/ (work in progress); removed .claude/ | decided by: User
2026-09-23 | Wrote OpenSpec change `build-mvp` (proposal, specs, design, tasks) for the MVP: Python + Pillow/imagehash/click/pytest, SHA-256 exact-hash + ahash near-dup detection, union-find grouping, CSV report; 4 capabilities: photo-scanning, exact-duplicate-detection, near-duplicate-detection, duplicate-report | decided by: User
2026-09-23 | Empty/no-matching-images folder is not an error: scan completes empty, pipeline reports zero duplicate groups; added scenario to photo-scanning spec and task 7.2 to build-mvp | decided by: User
2026-09-23 | Implemented and completed all build-mvp tasks (1.1-7.2): find_duplicates/{scanner,hashing,grouping,report,cli}.py, 23 passing tests; `duplicates.csv` is written next to (sibling of) the scanned folder, per README | decided by: User
2026-09-23 | Archived OpenSpec change build-mvp; its 4 capability specs (photo-scanning, exact-duplicate-detection, near-duplicate-detection, duplicate-report) are now the source of truth under openspec/specs/ | decided by: User
2026-09-23 | Wrote OpenSpec change `xlsx-report`: replace duplicates.csv with duplicates.xlsx (openpyxl) -- one stacked table per group (File, Similarity Score), blank-row separated, keep-file row highlighted; BREAKING change to duplicate-report capability | decided by: User
2026-09-23 | Implemented and archived xlsx-report; duplicate-report capability's "Write an Excel report" requirement is now the source of truth under openspec/specs/. Fixed a stale "CSV file" mention left in the capability's Purpose line, since archive doesn't rewrite Purpose from a delta | decided by: User
2026-09-23 | Cropped/edited photos are not detected as near-duplicates -- expected per README's explicit non-goal (rotated/cropped/heavily-edited duplicate detection), since average_hash isn't robust to cropping; left as a documented limitation, not fixed | decided by: User
2026-09-23 | Wrote OpenSpec change `similarity-categories`: replace raw Hamming-distance score with Exact/Very Similar/Similar labels; Exact = shared byte hash, Very Similar = distance <= threshold // 2, Similar = distance in (threshold // 2, threshold] | decided by: User
2026-09-23 | Implemented and archived similarity-categories. Fixed a bug found during manual verification: a mixed exact+near-duplicate group was labeled "Exact" if ANY pair shared an exact hash; now requires ALL members share the same exact hash | decided by: User
2026-09-23 | duplicates.xlsx silently overwrote an existing file with the same name -- discovered by testing. Wrote OpenSpec change `timestamped-report`: filename becomes duplicates_<YYYYMMDD>_<HHMM>.xlsx (minute precision, local time), and the CLI warns + prompts for confirmation before overwriting if that exact filename already exists | decided by: User

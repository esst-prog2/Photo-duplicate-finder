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

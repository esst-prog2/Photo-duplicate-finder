# Planning Log

Append-only. Format: `YYYY-MM-DD | decision | decided by: User or Claude`

2026-09-23 | Keep an append-only planning log in PLANNING_LOG.md, with its rules in AGENTS.md | decided by: User
2026-09-23 | Log line format: date, decision and decider, separated by " | " | decided by: Claude
2026-09-23 | Use OpenSpec as the spec tool; version still open (1.13.0 was asked for, but the latest release is 1.11.0) | decided by: User
2026-09-23 | Correction: real package is @fission-ai/openspec on npm (the bare "openspec" package is unrelated/defunct); 1.13.0 exists and installs cleanly | decided by: Claude
2026-09-23 | Installed OpenSpec 1.13.0 globally via npm and ran `openspec init --tools claude` in this repo | decided by: User
2026-09-23 | Redid OpenSpec init without AI-tool integration: ran `openspec init --tools none`, keeping only openspec/config.yaml (untouched), openspec/specs/ (source of truth), openspec/changes/ (work in progress); removed .claude/ | decided by: User

# AGENTS.md

Instructions for AI agents (and humans) working on this project.

## Planning log

Whenever we decide something about this project — a requirement, a number,
a name, a tool — append one line to `PLANNING_LOG.md`:

    YYYY-MM-DD | what was decided | decided by: User or Claude

Rules:
- One decision per line.
- Only append. Never rewrite, reorder, or delete an earlier line.
- If a decision changes, add a new line that says what replaced what
  (e.g. "threshold changed from 10 to 8") instead of editing the old one.
- "decided by" is User if the user made the call, Claude if Claude chose
  and the user did not decide it themselves.

## Process log

After each step that changes something in the project, commit it and add one
row to `PROCESS.md`, in the same commit:

    | the step | what the tool did | what the user decided |

Rules:
- One row per step, appended at the bottom. Never rewrite an earlier row.
- "What the user decided" is the user's own call. If the user decided nothing
  in that step, write "No decision" and name anything the tool chose on its own.
- A step that changes nothing (a question answered, a check with no edit) has
  nothing to commit and gets no row.
- Commit only. Push or open a pull request only when the user asks.
- To keep the rows in order and free of merge conflicts, put each new step on
  top of the previous step's branch, or on a fresh branch from the latest
  `main` once the previous one is merged.


# Start with TIE Studio

TIE Studio helps you clarify a consequential decision using project evidence, alternatives
and focused questions. The method is intended for use across AI coding agents; it does not require an added
hosted model API. This version supplies the Codex adaptation. Claude Code, Cursor and
other compatible hosts are intended future targets, not supported paths in this guide.

## Install in a disposable project

1. Authenticate Git access to `ericqian77/tie-studio-skill`, then clone the pinned snapshot
   into a new directory:

   ```sh
   git clone --branch review-2026.09.07.2 --single-branch https://github.com/ericqian77/tie-studio-skill.git tie-studio-review
   ```

   Inspect `README.md`, `LICENSE`, `MANIFEST.json` and `tie-studio/SKILL.md` before installing.
2. Choose a disposable project with no existing TIE Studio installation. Check both the
   project's `.agents/skills/` and your user Skill directory for existing Studio/Discovery
   copies. Resolve duplicates before proceeding; do not merge versions.
3. Copy the complete `tie-studio/` folder into `<project>/.agents/skills/tie-studio/`.
4. Open that project in a fresh Codex task and explicitly invoke `$tie-studio`:

> Use $tie-studio. Help me decide whether a short written guide or a live workshop
> would better help a small volunteer team learn our onboarding process. Inspect the
> project evidence first. Keep execution and publication outside this discussion.

Give real constraints and corrections. You should reach a meaningful distinction,
rejected alternative and explicit unknown, rather than merely a longer document.
To resume in a fresh task in the same project:

> Use $tie-studio. Resume the existing Session. Summarize the last settled decision
> and the next unresolved question without reopening settled work.

Project records belong under the project's `tie/`. The optional local TIE Workbench
opens only on explicit request; it is not necessary for the core decision workflow.
Python 3.9+ is needed for deterministic validators and the optional Workbench.
The Workbench server uses POSIX file locking on macOS/Linux; Windows parity is unproven.

## Upgrade, remove and roll back

Back up an existing installed Skill before replacement. Copy one complete reviewed
version, never merge trees. Preserve the project's `tie/`, decisions and Session IDs.
Remove only the installed Skill folder to uninstall. Restore its exact backup to roll
back; do not revert project decisions automatically. This candidate does not install,
start a service or update any existing installation by itself.

## Limitations and feedback

Structural tests do not prove judgment quality. Fresh-task continuation has required
assisted correction; watch for reopened decisions, lost uncertainty or permission drift.
No exact Codex client/model compatibility matrix has been established for this candidate.
Before wider delivery, verify install/start/correction/resume/uninstall in a clean Codex
project. Report version, host, expected behavior, observed behavior and assistance needed.
Share only voluntarily selected redacted excerpts; do not send credentials or full project records.

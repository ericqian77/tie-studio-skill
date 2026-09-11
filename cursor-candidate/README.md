# TIE Studio for Cursor — private candidate

**Pending real-host acceptance. This is not a supported release.**

Candidate `2026.09.07-cursor-candidate.1` contains 28 Skill files generated from the
same shared method as the Codex adaptation. Its shared core is
`2026.09.06.2-extracted.1`; host instructions and installation identity are separate.

Start with [START_HERE.md](START_HERE.md). Review [ACCEPTANCE.md](ACCEPTANCE.md),
[the host manifest](HOST_MANIFEST.json), [source provenance and distribution hashes](DISTRIBUTION_MANIFEST.json)
and [LICENSE](LICENSE). Run `python3 -B verify.py` before copying the Skill.

This directory is an additive candidate on branch `codex/cursor-candidate-20260910`.
The repository's root `tie-studio/`, root installation guide, existing Codex main and
`review-2026.09.07.2` are unchanged. Do not use the root Codex package for this trial.
The development repository is the only method source. Report fixes there and rebuild;
do not maintain edits solely in an installed or distributed copy.

## Known discovery blocker

On September 7, 2026, Cursor 3.19.13 on macOS discovered an existing user-level Codex
TIE Skill while the project candidate did not appear in the inspected project scope.
The candidate's file-copy checks passed. Correct candidate loading, invocation,
correction and new-chat recovery have **not** passed. A GitHub clone provides a
traceable installation source; it does not fix or prove discovery isolation.

Keep other hosts intact. Do not remove a Codex installation, enable automatic rules,
change permissions or choose an ambiguous same-name entry to make the trial pass.
Live Workbench open/refresh/stop is unavailable until instance isolation is implemented.
CLI, Cloud Agents, remote workspaces and Windows are not validated.

Hashes detect drift, not publisher authenticity. Clone the identified private repository
with your own GitHub access and record the exact distribution commit used for the trial.

# TIE Studio

A portable decision method and Skill for AI coding agents, built around Taste, Intent
and Eval.
Start from project evidence, compare useful alternatives, preserve uncertainty, and
carry decisions across tasks before authorizing substantial execution.

**Repository status: private review.** This repository is an independently packaged
snapshot for owner review and installation experiments. Public release is pending.

- Skill version: **2026.09.06.2**
- Distribution snapshot: **2026.09.07-review.2**
- Installation ref: **review-2026.09.07.2**
- License: [MIT](LICENSE)

## Product direction and current host support

TIE Studio is designed to work across AI coding agents, with Codex, Claude Code,
Cursor and other compatible agent hosts as intended integration targets. The decision
method and project records are intended to remain portable; each host needs its own
installation, invocation and tool-permission adaptation.

**This version provides the Codex adaptation.** Claude Code, Cursor and other hosts
are future compatibility targets, not supported installations promised by this snapshot.
Existing compatibility experiments do not establish equivalent behavior across hosts.
The first implementation target does not define the product's long-term identity.

## Install with Codex

Give Codex this instruction in the project where you want to try the Skill:

> Use the skill installer to install TIE Studio from repository
> ericqian77/tie-studio-skill, path tie-studio, ref review-2026.09.07.2.
> Install into this project's .agents/skills directory. Check for existing Studio
> or Discovery installations first and do not overwrite them without a backup.

The repository is private, so the installing environment needs an account with access.
A URL alone does not grant access. See [START_HERE.md](START_HERE.md) for manual
installation, first use, recovery, upgrade and removal.

After installation, explicitly invoke `$tie-studio`. For existing work:

> Use $tie-studio. Resume this project's existing TIE Session and identify the next
> unresolved decision without reopening settled work.

## What is included

The complete `tie-studio/` folder includes the method instructions, four work-type
modules, empty artifact templates, deterministic validators and an optional local
TIE Workbench with English and Chinese interface resources. No hosted model API or
additional model runtime is required; reasoning stays with the current Codex host.

Workbench is optional and opens only when requested. Its current server implementation
uses Python 3.9+ and POSIX file locking on macOS/Linux. Windows parity is not established.
Project records remain in each user's own `tie/` directory.

## Read and review

- [Main Skill instructions](tie-studio/SKILL.md)
- [Discovery method](tie-studio/references/discovery.md)
- [Decision quality and approval boundaries](tie-studio/references/decision-quality.md)
- [Workbench instructions](tie-studio/references/dashboard.md)
- [Synthetic correction/resume example](EXAMPLE.md)
- [Exact payload hashes](MANIFEST.json)

This distribution contains no private development history or real project records.
The manifest covers every payload file except itself.

## Limits and maintenance

Deterministic checks do not establish judgment quality or long-term reliability.
Fresh-task continuation has needed assisted correction. Clean host-agent acceptance
and a precise Codex client/model compatibility matrix remain unproven for this snapshot.
Other hosts are not equally validated. Host privacy/network policies still apply.

This repository is a derived release surface. Improvements are reconciled in the
canonical development source before exporting another reviewed snapshot. Do not assume
that main is the same as a pinned version. Accepted external contributions should retain
attribution when incorporated. No automatic project-data collection is included.

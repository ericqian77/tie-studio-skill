# TIE Studio for Cursor

**Make consequential decisions before you build.**

TIE Studio is a decision Skill built around **Taste, Intent, and Eval**. It helps you
clarify what you want, compare meaningful alternatives, and define what a good result
would look like—inside the project where you work.

**Preview · MIT licensed.** Package version `2026.09.11-preview.1`.
Cursor project discovery has an unresolved issue; conversational acceptance is pending.
Read [Compatibility and validation](ACCEPTANCE.md) before trying it.

[Install](START_HERE.md) · [Compatibility](ACCEPTANCE.md) · [Changes](CHANGELOG.md) · [Contribute](CONTRIBUTING.md) · [License](LICENSE)

## What it helps you do

- Clarify the purpose behind a proposed feature, piece of writing, research project or presentation.
- Compare alternatives with real consequences and keep unproven assumptions visible.
- Correct your direction while preserving decisions that still apply.
- Keep project-local records so another conversation can recover the decision and next question.

These are the method's intended capabilities. Packaging checks have passed; this Cursor
preview has not yet passed the complete start, correction and fresh-chat recovery workflow.

## A first conversation

After installation and confirmation that Cursor has loaded this project's Skill,
explicitly select `/tie-studio` and send:

> Help me decide whether a short guide or a live workshop would better help our
> volunteer team. Read the project evidence first. Do not implement anything yet.

Later, you can correct the goal:

> The goal is comparing conflicting experiences, not faster onboarding.
> Save this correction and pause; do not build.

Project decisions stay in `tie/`. A new conversation should resume those records rather
than create a duplicate Session. Approval of a discussion or plan does not authorize execution.
See the [validation scenarios](ACCEPTANCE.md) for how to check these behaviors.

## One method, independent integrations

The Cursor and Codex packages are generated from one shared decision method, with their
own host instructions, version pins and installation paths. You install the complete
package for your host. Host-specific updates can be tested and rolled back separately.

Independent packages do not guarantee independent discovery: Cursor may also find Skills
installed for other hosts. Confirm the actual loaded path and preserve those installations.
Live Workbench is unavailable in this preview. The ordinary workflow is text-based.

## Share this package

The standalone ZIP contains this guide, installation instructions, the Skill, MIT license
and checksums. It can be handed to another user without development project records,
private conversations or access to the development repository. Keep the license and
validation-status documents with it. The MIT text is in [LICENSE](LICENSE).

No additional hosted inference service is included. The Skill runs inside the recipient's
Cursor environment, using its model, tools and permissions. A private GitHub repository
still requires access; distributing a ZIP does not change the repository's visibility.

## Verify and report

Run `python3 -B verify.py` from the extracted package. The manifests record the exact
Skill payload, source commit and file hashes. Checksums detect modifications; obtain the
package through a source you trust. Share redacted issues using [CONTRIBUTING.md](CONTRIBUTING.md).

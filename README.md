# TIE Studio

**Make consequential decisions before you build.**

A portable decision Skill for AI coding agents, built around **Taste, Intent, and Eval**.
Read project evidence, compare meaningful alternatives, preserve uncertainty, and carry
accepted decisions into the next conversation. Reasoning stays in your coding agent;
no additional hosted model service is required.

**Open-source preview · MIT licensed.** Choose the package for your host:

| Host | Package | Status | Install |
| --- | --- | --- | --- |
| Codex | `tie-studio/` · `2026.09.06.2` | Existing adaptation; clean-host compatibility matrix incomplete | [Codex instructions](CODEX_INSTALL.md) |
| Cursor | `cursor/tie-studio/` · distribution `2026.09.11-preview.1` | Preview; project discovery unresolved, conversation acceptance pending | [Cursor instructions](cursor/START_HERE.md) |
| Claude Code | Not supplied | Planned, not validated | No installation package yet |

## Install through your agent

For Cursor, paste this into an Agent conversation with terminal and file access:

```text
Install TIE Studio for Cursor from https://github.com/ericqian77/tie-studio-skill.
Clone the repository into a new download directory outside my project and Skill
installation directories. Record the commit and run `python3 -B verify.py` from
its root. Then follow cursor/START_HERE.md, including package verification.
Use a new test project, leave other host installations untouched, and tell me
how to confirm the actual loaded Skill source. Do not install the root Codex package.
```

This is an instruction for your agent to read and execute the documented installation,
not a marketplace installer or proof of successful Cursor discovery. If your agent
cannot download or write files, use the [manual instructions](START_HERE.md).
For repeatable trials, retain the downloaded commit; `main` can change.

**Known Cursor issue:** a prior local trial found the global Codex Skill instead of
the intended project Skill. Confirm the loaded path before invoking `/tie-studio`.
Copying files or seeing the same name is insufficient. See [acceptance evidence](cursor/ACCEPTANCE.md).

## Try a consequential decision

After confirming the correct installation, explicitly invoke the Skill (`$tie-studio`
in Codex or `/tie-studio` in Cursor) and ask:

> Help me decide whether a short guide or a live workshop would better help our
> volunteer team. Read the project evidence first. Do not implement anything yet.

Correct the goal as you learn. Project decisions live in your project's `tie/` directory.
In a fresh conversation, explicitly invoke the Skill and ask it to resume those records.
These are intended behaviors; deterministic checks do not prove judgment quality or
reliable recovery. Approval of a discussion does not authorize implementation.

## Shared method, independent packages

Both packages derive from one maintained method with separate host instructions,
version pins, acceptance and rollback. Updating one installation does not update another.
Host discovery can still expose same-name Skills across locations; verify their sources.
Concurrent writes to the same project decision records are not supported.

The optional Codex Workbench uses Python 3.9+ and POSIX file locking; Windows parity is
unproven. Live Workbench is disabled in the Cursor preview. Neither package requires it
for the ordinary text workflow. Host permissions and network policies continue to apply.

## Downloads, integrity and feedback

- [Standalone Cursor ZIP](downloads/tie-studio-cursor-2026.09.11-preview.1.zip) · [SHA-256](downloads/tie-studio-cursor-2026.09.11-preview.1.zip.sha256)
- [Synthetic correction/resume example](EXAMPLE.md)
- [Repository manifest](MANIFEST.json): run `python3 -B verify.py` in a clean download.
- [Feedback and contributions](CONTRIBUTING.md) · [MIT license](LICENSE)

The original Codex snapshot remains pinned at `review-2026.09.07.2`; its historical
private-review wording describes that snapshot. Current repository presentation does
not change its Skill payload. Cursor's embedded provenance also retains its original
preview identity. A public preview is not a stable host-support claim.

This is a derived distribution repository. It includes no real project decision records.
Method changes are maintained in the development source and exported as reviewed
packages. Public installation does not require access to that development repository.

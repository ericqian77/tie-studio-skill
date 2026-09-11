# Cursor host contract

Candidate: 2026.09.07-cursor-candidate.1. Shared method: 2026.09.06.2-extracted.1.
G2 prepares the package; real Cursor discovery, invocation, correction and recovery
have not been accepted. This is not a claim of general Cursor support.

## Explicit activation and continuation

The user explicitly selects `/tie-studio` in Agent chat or explicitly activates this
same Skill as a Custom Mode. Either satisfies the shared method's explicit-invocation
boundary; merely mentioning Taste, Intent or Eval does not. Do not create always-on
rules, silently activate a mode, or rely on Codex's `agents/openai.yaml`.

A normal slash invocation attaches the Skill to one message. For a continuing discussion,
the user may select it as a Custom Mode; verify the active mode in the actual UI. Do not
infer persistent loading from a normal slash selection. When persistent mode is unavailable,
explain the per-message limitation and have the user explicitly reselect the Skill for
subsequent turns; do not silently change host settings to compensate.

Exiting the mode stops the persistent host context; it neither deletes project records
nor revokes unchanged decisions. Saving/pausing the work is a separate user request.
A fresh chat explicitly selects the Skill again, reads the owning workspace's TIE and
existing Session, and resumes the saved point without a new Session or repeat interview.
Mode activation, agreement, `continue` and successful tool calls never grant execution
approval. Keep the common Blueprint, handoff and actual-execution gates intact.

## Workspace, resources and tool permissions

Resolve the Skill root from the actual loaded SKILL.md location and verify its resources.
The intended project installation is `<project>/.cursor/skills/tie-studio/`. That is a
candidate location, not proof of which installation Cursor loaded. If the source is
ambiguous or multiple copies are discovered, report the conflict; do not guess precedence
or remove another host's copy. Directory separation alone does not ensure discovery isolation.

Keep three paths distinct: the loaded Skill root, the user's project root, and the selected
`<project>/tie/sessions/<id>/`. Discover Sessions in that project only; do not treat installed
Skill templates, nested fixture repositories or the development checkout as user state.
Use workspace-qualified Session identity when ambiguity matters. Same-outcome continuation
keeps the same records across chats. Do not have two hosts write one Session concurrently;
explicitly finish/save the previous writer before handing the work over.

Use Cursor's available native file reading, search, editing and terminal tools. Do not
assume Codex-specific tools, MCP servers or background tasks exist. Resolve resources
relative to the loaded Skill, not the shell's current directory. In command examples,
`TIE_SKILL_ROOT` means that verified absolute directory; set it explicitly with safe shell
quoting, never copy the placeholder as an actual project path:

```sh
TIE_SKILL_ROOT='/absolute/path/to/project/.cursor/skills/tie-studio'
TIE_PROJECT_ROOT='/absolute/path/to/project'
python3 "$TIE_SKILL_ROOT/scripts/validate_artifacts.py" --templates "$TIE_SKILL_ROOT/assets"
python3 "$TIE_SKILL_ROOT/scripts/validate_artifacts.py" --project "$TIE_PROJECT_ROOT"
```

The shared entry's shorter validation examples assume the Skill root as the working
directory; use the absolute form above from other directories. Python 3.9+ is required
for these bundled checks. If absent, state that checks are unrun; do not install a runtime
or claim validation succeeded. Copying the Skill itself needs no Python or Node.

Keep the current host's permissions and approval controls. Do not turn a tool denial into
an instruction to weaken settings or bypass `.cursorignore`. If permitted native writing
or terminal tools are unavailable, explain the affected action and provide a reviewable
text result or command without pretending it ran. No hosted model API is added by this
Skill; project evidence is processed by the user's current Cursor/model environment.

The `codex-recommended-provisional` and `codex-recommended-user-confirmed` values are
legacy record-format labels for agent-proposed routing, not evidence of the actual host.
Preserve these enum values; record actual Cursor/user provenance in the existing evidence
fields. Do not rename historical decisions or auto-migrate project records.

## Live Workbench unavailable in this candidate

Common Workbench resources are bundled unchanged so there is one implementation. Its
current service identity is shared by project/Session, and cross-host process/cache
isolation is not implemented here. Live Workbench is not enabled for this Cursor candidate.
On an explicit open/refresh/stop request, explain this capability limit and preserve the
project records; do not start, attach to, refresh or stop a live instance through Cursor.
Do not reuse or stop a possible Codex service. Do not imply that this blocks ordinary
text-first decisions or validation. A later G4 candidate must implement and validate
instance isolation before enabling these live operations. No new UI or runtime is created.

## Documentation basis and evidence limits

Official documentation checked 2026-09-07: [Agent Skills](https://cursor.com/docs/skills)
and [Agent Security](https://cursor.com/docs/agent/security). The documented slash/Mode
mechanisms and host permission controls are inputs to this adapter, not runtime evidence.
Cursor also discovers compatible host directories; G3 must inspect actual loaded copies.
Initial acceptance target is local macOS Cursor. CLI, Cloud Agents, remote workspaces,
Windows, GitHub import and other hosts are not validated by this candidate.

# Cursor candidate: installation, upgrade and rollback

Version: 2026.09.07-cursor-candidate.1. G2 local candidate; not installed or host-accepted.
Use this guide only after a separately authorized project-local installation request.
Installation does not start a TIE discussion, create project records, or enable Workbench.

1. Identify the selected low-risk project and the exact candidate's parent MANIFEST.json.
   Verify every `files` entry against the adjacent `tie-studio/` folder, including the
   complete member set. Reject extra/missing files or symlinks. Hashes establish identity,
   not publisher authenticity; obtain the candidate from its trusted source.
2. Inspect the project's destination `.cursor/skills/tie-studio/` and its ancestors for
   symlinks. Stop if the path is unclear or an existing installation would be overwritten.
   Inspect project, nested, ancestor, user and plugin discovery scopes, including compatible
   `.agents`, `.codex` and `.claude` directories, for TIE copies. Do not guess precedence.
3. Keep staging and backups outside all discovered Skill roots. Copy the complete verified
   `tie-studio/` folder into the project only. Do not copy the development `core/`/`adapters/`
   source tree or merge folders. Do not modify any global Skill, settings, sync or plugin.
4. Verify the copied member set and all hashes again. In Cursor, verify a unique intended
   entry and actual source. If loading is absent/ambiguous, record version/UI evidence and
   stop before workflow acceptance. Reopening a chat is not proof of correct loading.
5. Starting discussion requires the user's explicit `/tie-studio` selection or explicit
   activation as Custom Mode. See `references/cursor-host.md`; live Workbench stays disabled.

These are preflight instructions, not an automatic installer's safety enforcement. A clean
profile alone does not prove separation from user/global discovery paths. Simultaneous
Codex/Cursor installation needs its own G3 coexistence evidence; never delete a working
Codex installation just to obtain a clean Cursor result.

For an upgrade, first identify the exact old Cursor folder, save its manifest and hashes,
and move only that folder to a unique backup outside discovery roots. Verify the new complete
package before copying. Open a fresh chat for the new version; old chats retain earlier context.
If a check fails, restore the exact old Cursor folder and verify its hashes. Do not merge old
and new files. This candidate does not launch a service, so it owns no live Workbench to stop.

For uninstall, move only the identified Cursor folder to a recoverable backup outside
all discovery roots; then verify its absence in a fresh Cursor chat. Preserve `tie/`,
Sessions, Blueprints, approvals, unrelated project work and every other host's installation.
Do not automatically revert decision records when rolling back the Skill. Keep the separate
manifest with the rollback copy. No remote repository update follows from installation.

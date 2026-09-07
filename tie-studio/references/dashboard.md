# Optional local dashboard (P2)

This optional reading surface belongs to the selected project and existing Session.
It does not own decisions, run a second interview or change approval boundaries.
Use only for an explicit dashboard request. Ordinary Discovery remains unchanged.
Natural-language requests are interpreted by the current host agent. There is no
second model, text-trigger daemon or separate Skill. The helper provides publish,
serve, status and stop as well as offline validate/render.

## Host responsibilities

1. Resolve the current project and Session using their governing records. A root
   PROJECT_STATE pointer is evidence about location, not automatic semantic authority.
   Read only relevant files in the selected source workspace. Never silently combine
   projects or infer a new Session from a new conversation.
2. Read the current understanding, decisions, unknowns and relevant evidence. Author
   English-default summaries that preserve scope and authority. Use `view.schema.json` as a
   private output contract. Do not migrate canonical files to satisfy it.
3. Record the complete SHA-256 of each source's UTF-8 bytes, a relative path and its
   source language. Citations use inclusive one-based lines and the exact lines joined
   by LF, without a trailing newline. File fingerprints still include original bytes.
4. Keep authority, evidence and lifecycle separate. `verified` requires a cited check
   that actually verifies that claim; structural validation is not semantic approval.
   `reported` is a result in another report. `unverified` preserves the missing evidence.
5. Use host-generated stable display IDs or existing IDs. Classifications are reading
   aids. Source-recorded connections need citations; host-organized connections are
   labeled interpretations. Do not invent a causal network.
6. Author events in recorded order, using known dates or explicit order labels. Before
   and after statements each need their own citations. If no earlier statement is
   available use `before: null`. Linked records show the captured current record, not
   an invented full past state. Describe history and selection coverage honestly.
7. Finish source reconciliation before capture, including current record implications,
   unresolved choices and stage/next-step pointers, not only the overview. Retain valid
   decisions while replacing obsolete "not yet approved" implications after later approval.
   Historical limits need their original time/scope. Use `reconciliation: pending` when
   contradictions remain; matching hashes do not establish semantic coherence.
8. Default UI and derived summaries to English regardless of conversation/source language.
   An explicit view-language request overrides that default for this enabled view. Preserve
   source excerpts exactly. Never translate enum values. `uiLocale` selects shared UI
   resources (`en` or `zh-CN`); `summaryLocale` declares the host-authored summary language
   independently. Paraphrase uncertainty stays visible in either language.

## English and Chinese with one runtime

"Show this workbench in Chinese" means author Chinese reading summaries and set both
`uiLocale` and `summaryLocale` to `zh-CN`, unless the user requests only UI translation.
For UI-only switching, change `uiLocale` and retain the actual `summaryLocale` and content.
Use `en` to switch back; translate summaries only when requested, retaining IDs, scope,
authority and citations. Remember this view preference on subsequent source refreshes.
Source language and the project's deliverable language do not change with this view.

Validate and publish through the same CLI/server. An open live view receives the new
messages and content on its next source check, retaining valid selection, search, detail
tab and reading position. Repeated `serve` reuses the same instance; no restart or copied
runtime directory is needed for language changes. Static exports require re-rendering.
Unknown locales fail clearly. Changing a locale field does not translate prose; the host
must author any requested translation. Browser polling never calls a model.

An older project-local runtime must be upgraded under its own install authority before
it can use this support. Do not modify another project's installation or silently migrate
its custom Chinese runtime simply because the source Skill now supports both languages.

## Host flow: open, refresh, close and stop

- **Open the TIE dashboard:** after explicit invocation of the parent Studio, resolve the
  current project and existing Session. Read the records and author `view.json` as above.
  Validate, publish, then `serve`. Repeated `serve` reuses a matching authenticated
  instance. Show its returned local URL in an allowed host surface or as a user link.
- **Refresh the TIE dashboard:** finish canonical updates/reconciliation; read every
  relevant changed source and reconsider affected summaries, evidence and relationships.
  Publish a newly validated view using stable IDs for surviving records. The open page
  detects the revision and updates without clearing the view, search or surviving selection.
  Never only refresh hashes to make stale summaries pass. No `serve` is needed unless
  the user also asks to reopen a stopped dashboard.
- **While enabled:** after relevant source edits in the authorized conversation, update
  the projection as part of that turn. An idle host does not run semantic refreshes.
  Source changes made elsewhere are detected when the page polls or status is queried;
  they do not initiate background model work.

- **Close the dashboard:** close the current tab if the host supports it, or tell the
  user to close it. Closing the tab does not kill the local service.
- **Stop the dashboard service:** run `stop` for this exact project/Session. Verify its
  result. Do not kill a PID from a stale file or use broad process-name matching. A
  stopped service requires a new explicit open request to restart.

Reuse stable IDs and unaffected reading content; reconsider the summaries and relationships
whose meaning changed, then update exact excerpts/line ranges when source positions move.
Do not rebuild several full project narratives for each short answer. Source changes
during preparation require rereading and reconciliation before publication, not replacing
newer records or refreshing only hashes. Full Blueprint compilation remains lazy.

## Commands

Python 3.9+ standard library on macOS/Linux (POSIX file locking); no new dependencies.
`--project` is the explicit source workspace; `--session` is its existing Session ID.
The host-authored input may be in an authorized output directory. Working copies and
process metadata are private, ignored, rebuildable files under
`<project>/.tie-cache/dashboard/<session>/`.

```bash
python3 skills/tie-studio/scripts/tie_dashboard.py validate \
  --project /path/to/project --view /path/to/view.json
python3 skills/tie-studio/scripts/tie_dashboard.py publish \
  --project /path/to/project --session main --view /path/to/view.json
python3 skills/tie-studio/scripts/tie_dashboard.py serve \
  --project /path/to/project --session main
python3 skills/tie-studio/scripts/tie_dashboard.py status \
  --project /path/to/project --session main
python3 skills/tie-studio/scripts/tie_dashboard.py stop \
  --project /path/to/project --session main
```

`serve` returns a loopback URL, reuses an existing instance, or starts a process bound
only to `127.0.0.1`. Optional `--port` requests a port; if occupied an available port
is selected. Starting needs permission to bind a local socket in restricted hosts.
The private URL is a local access capability; do not include it in public reports.
Only the dashboard and its fixed state/identity endpoints are served, with a private
instance route, exact Host checks and same-origin enforcement. No project directory
or arbitrary path endpoint is exposed. Stop is an authenticated local lifecycle action;
there are no source-edit, approve, deploy or model endpoints.

## Freshness and recovery

The page checks included source files approximately every two seconds while open.
The command-line `status` also checks on demand. There is no constant full-project
scan or background reasoning. The states are separate:

- **Source versions match:** the published view's included file versions match. This
  is not proof of semantic accuracy, decision approval or unrecorded chat coverage.
- **Summary needs refresh:** sources changed; the old published summary stays visible.
  Ask the project agent to refresh. The browser's **Check sources** button only checks.
- **Records need reconciliation:** the host published a pending reconciliation state.
- **Source unavailable:** an included source moved, disappeared or cannot be read.
- **Update could not be loaded:** preserve the last valid in-memory view if a cache
  update is malformed or invalid. Re-author and publish a valid view to recover.
- **Service unavailable:** the page cannot check files. Reopen through the host; a
  restarted instance returns a new URL. Never display stale content as live-current.

Schema, references, exact excerpts and fingerprints are checked on publication. Failed
publication leaves the previous cache untouched. If a source changes immediately after
publication it is marked stale on the next check. The running service keeps the last
valid view when an invalid candidate appears; it does not silently adopt broken content.

Stop before removing disposable cache files. A stale process record is never treated
as permission to signal its PID. Correctly scoped stopped records may be replaced by a
new instance; malformed identity records fail clearly instead of contacting an arbitrary
endpoint. Keep canonical records intact when recovering or deleting a view.

## Static export and remaining boundaries

`render --project /path/to/project --view /path/to/view.json --output /path/to/view.html`
still writes an offline snapshot. It contains no network client and does not watch files.
Live updates are not retrospectively added to old exported files.

No full historical archive, arbitrary point replay, real-project install, global update
or package release is included. Existing frozen builders retain their old contracts.
Follow browser policy when showing or inspecting a view; a new local transport must
not be used to bypass an earlier inspection denial. HTTP service tests are mechanical
functionality checks, not a substitute for allowed actual-browser acceptance.

## Review before delivery

Walk from overview to a record, a relationship, its source and back. Check a recorded
change and its historical coverage. Search including original-language words, inspect
inactive records in the directory, and compare the summaries with source authority.
Mechanical checks cannot establish reader usefulness, responsive layout or focus
behavior; browser checks and semantic review remain separate evidence.

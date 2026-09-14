# Install TIE Studio for Cursor

Version `2026.09.13-preview.1`. Local macOS is the initial acceptance target.
**Known issue:** correct project Skill discovery is unresolved. Verify the loaded source
before starting a conversation. See [Compatibility](ACCEPTANCE.md).

## 1. Get the package

Clone from GitHub into a new download directory:

```sh
git clone --branch main --single-branch https://github.com/ericqian77/tie-studio-skill.git tie-studio-cursor-download
cd tie-studio-cursor-download
git rev-parse HEAD
python3 -B verify.py
cd cursor
```

Record the printed commit so the downloaded version can be identified. This public
repository also includes a Codex package at its root; use this `cursor/`
directory for Cursor. Keep the download outside your actual project and Skill discovery roots.

## 2. Verify and install into a new project

Python 3.9+ is required for these checks. No package dependencies are installed.
First run:

```sh
python3 -B verify.py
```

Stop if verification fails. Then, from the same folder, run:

```sh
python3 -B - <<'PYTHON'
from pathlib import Path
import shutil
from verify import verify

package = Path.cwd()
verify(package)
project = Path.home() / 'tie-cursor-preview'
project.mkdir()  # Refuse an existing project; do not merge installations.
target = project / '.cursor' / 'skills' / 'tie-studio'
target.parent.mkdir(parents=True)
shutil.copytree(package / 'tie-studio', target)
verify(package, target)
print('Open in Cursor:', project)
print('Expected loaded Skill:', target / 'SKILL.md')
PYTHON
```

If the project already exists, choose a new project name by editing the `project` line
before running the block. Do not repeat recursive copies into an existing Skill folder.
Installing does not create TIE decision records or enable a live Workbench.

## 3. Confirm the source, then start

Open the printed project folder in Cursor and reload the window. Inspect the discovered
`tie-studio` entry's actual source. It must be the printed project's `.cursor/skills` path.
A matching name, a User skill label, or successful file copying does not establish this.

If only another host's global entry appears, the project entry is absent, or source
selection is ambiguous, stop and report that observation. Do not delete another host's
installation, change permissions or add automatic rules to bypass the issue.

Once the correct source is established, explicitly select `/tie-studio` and use the
[first conversation](README.md#a-first-conversation). A slash invocation attaches to
one message. Persistent Custom Mode behavior still requires real-host validation;
see the packaged [host guidance](tie-studio/references/cursor-host.md).

## Update or remove

Before updating, save the current Session and back up the exact installed folder outside
all discovery roots. Verify the new complete package, then replace the old folder as a
unit. Never merge folders or use `git pull` to update a live installation automatically.

To uninstall, move only the identified `.cursor/skills/tie-studio` installation out of
the project's discovery scope. Preserve project `tie/` decisions, other hosts and settings.
Start a fresh chat and inspect discovery again. Rollback restores a complete verified
Skill folder; it does not roll back the user's decisions.

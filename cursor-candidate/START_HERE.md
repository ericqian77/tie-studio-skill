# Install the private Cursor candidate

Status: **pending real-host acceptance**. Keep this clone outside your test project
and all host Skill discovery directories. Commands below are for a local macOS shell.
They do not require installing dependencies. Python 3.9+ is needed for verification.

## Download and verify

From a directory where `tie-studio-cursor-download` does not already exist:

```sh
git clone --branch codex/cursor-candidate-20260910 --single-branch https://github.com/ericqian77/tie-studio-skill.git tie-studio-cursor-download
cd tie-studio-cursor-download
git rev-parse HEAD
cd cursor-candidate
python3 -B verify.py
```

Stop on any error. Save the printed Git commit; a branch name can move. Review the
manifest, this guide and `tie-studio/INSTALL.md`. The root repository guide describes
Codex; use this directory's guide for Cursor. Do not open the download clone as the
trial project: it contains both host packages.

## Copy into a new disposable project

Remain in the verified `cursor-candidate` directory. The following block creates a
new project and refuses an existing destination. It copies only the Cursor Skill,
not the distribution clone, and does not alter global installations or create TIE records.

```sh
python3 -B - <<'PY'
from pathlib import Path
import shutil
from verify import verify

package = Path.cwd()
verify(package)
project = Path.home() / 'tie-cursor-trial-20260910'
project.mkdir()  # Stop if this project already exists; do not merge installations.
target = project / '.cursor' / 'skills' / 'tie-studio'
target.parent.mkdir(parents=True)
shutil.copytree(package / 'tie-studio', target)
verify(package, target)
print('Open this project in Cursor:', project)
print('Expected loaded Skill:', target / 'SKILL.md')
PY
```

Open only that new project in Cursor and reload its window. Inspect the discovered
Skill's source before sending a prompt. It must be the printed project `.cursor/skills`
path. A `User skill` label, the name `tie-studio` alone, or successful copying does not
prove this. Cursor may also discover Codex/Claude/global/plugin copies. If only the
Codex source appears, the project entry is missing, or selection is ambiguous, stop
and record the version, scope and observed source. Do not delete another host's Skill.

Once actual candidate loading is confirmed, follow [ACCEPTANCE.md](ACCEPTANCE.md).
Installing alone does not approve a Blueprint, implementation, external action or Workbench.

## Rollback and updates

Close or pause the trial conversation first. To uninstall, move only the identified
project `.cursor/skills/tie-studio` folder to a unique backup outside all discovery roots.
Keep the manifest beside the backup. Preserve any project `tie/` records, approvals,
other host installations and global settings. Open a fresh chat and inspect discovery
again. Absence of an entry that was never observed is not proof of successful UI removal.

For updates, clone a new pinned candidate into a fresh download directory, verify it,
back up the exact old installation and copy the new complete folder. Never copy into
an existing Skill folder: repeated recursive copies can create nested duplicate Skills.
Do not use `git pull` as an automatic update of a live installation.

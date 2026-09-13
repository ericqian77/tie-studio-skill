# Install TIE Studio

Choose the host first. Python 3.9+ is required for deterministic checks.

## Download and verify

Clone into a new directory outside your project and Skill discovery directories:

```sh
git clone https://github.com/ericqian77/tie-studio-skill.git tie-studio-download
cd tie-studio-download
git rev-parse HEAD
python3 -B verify.py
```

Record the commit. Stop if verification fails. While the repository is private, Git
requires access; after publication, anonymous cloning is sufficient. Do not run
`git pull` inside an installed Skill directory.

## Cursor

Read and follow [cursor/START_HERE.md](cursor/START_HERE.md) beginning with step 2
from the downloaded `cursor/` directory. Its standalone verifier must also pass.
Install only `cursor/tie-studio/` into a new project's `.cursor/skills/tie-studio/`.
Confirm the actual loaded source; do not substitute a global Codex installation.
See [known limitations](cursor/ACCEPTANCE.md). The installation demo and real-host
acceptance occur after public distribution; they are not yet recorded as passing.

## Codex

Follow [CODEX_INSTALL.md](CODEX_INSTALL.md). The original pinned snapshot and root
`tie-studio/` payload remain available. Do not install the Cursor package into Codex.

## Updates and removal

Back up the exact installed Skill outside discovery directories before replacing it
with a complete verified package. Never merge package folders. Preserve your project's
`tie/` records and other hosts. Uninstall only the identified host's Skill folder.

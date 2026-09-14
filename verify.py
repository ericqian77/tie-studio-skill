#!/usr/bin/env python3
"""Verify a clean repository download, including both host packages."""
import hashlib
import json
from pathlib import Path
import runpy


def verify(root):
    root = Path(root).resolve()
    manifest = json.loads((root / 'MANIFEST.json').read_text())
    actual = {}
    for path in root.rglob('*'):
        name = path.relative_to(root).as_posix()
        if name == '.git' or name.startswith('.git/'):
            continue
        if path.is_symlink():
            raise ValueError('Unexpected symlink: ' + name)
        if path.is_file() and name != 'MANIFEST.json':
            actual[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != manifest['files']:
        raise ValueError('Repository has missing, extra or changed files; use a clean download')
    cursor = runpy.run_path(str(root / 'cursor/verify.py'))['verify'](root / 'cursor')
    return {'repository_files': len(actual) + 1, 'cursor': cursor,
            'codex_payload': manifest['hosts']['codex']['version'],
            'status': 'integrity-passed; real-host acceptance is separate'}


if __name__ == '__main__':
    print(json.dumps(verify(Path(__file__).parent), indent=2))

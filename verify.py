#!/usr/bin/env python3
"""Verify a clean repository download, including both host packages and the Cursor ZIP."""
import hashlib
import json
from pathlib import Path
import runpy
import zipfile


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
    archive = root / 'downloads/tie-studio-cursor-2026.09.11-preview.1.zip'
    expected = archive.with_suffix('.zip.sha256').read_text().split()[0]
    if hashlib.sha256(archive.read_bytes()).hexdigest() != expected:
        raise ValueError('ZIP checksum mismatch')
    with zipfile.ZipFile(archive) as zipped:
        entries = zipped.namelist()
        expected_files = {p.relative_to(root / 'cursor').as_posix(): p.read_bytes()
                          for p in (root / 'cursor').rglob('*') if p.is_file()}
        if len(entries) != len(set(entries)) or set(entries) != {'tie-studio-cursor/' + n for n in expected_files}:
            raise ValueError('Unexpected archive inventory')
        for name, data in expected_files.items():
            if zipped.read('tie-studio-cursor/' + name) != data:
                raise ValueError('ZIP/package mismatch: ' + name)
    return {'repository_files': len(actual) + 1, 'cursor': cursor,
            'codex_payload': manifest['hosts']['codex']['version'],
            'status': 'integrity-passed; real-host acceptance is separate'}


if __name__ == '__main__':
    print(json.dumps(verify(Path(__file__).parent), indent=2))

#!/usr/bin/env python3
"""Read-only package integrity check. Does not install, invoke a model or prove host support."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate manifest key: ' + key)
        result[key] = value
    return result


def inventory(root):
    if not root.is_dir() or any(p.is_symlink() for p in [root, *root.parents]):
        raise ValueError('Missing directory or symlink: ' + str(root))
    result = {}
    for p in root.rglob('*'):
        if p.is_symlink():
            raise ValueError('Symlink: ' + str(p))
        if p.is_file():
            result[p.relative_to(root).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    return result


def check_paths(files):
    for name, checksum in files.items():
        path = PurePosixPath(name)
        if not name or path.is_absolute() or '..' in path.parts or str(path) != name or '\\' in name or name == '.':
            raise ValueError('Unsafe manifest path')
        if not isinstance(checksum, str) or len(checksum) != 64 or any(c not in '0123456789abcdef' for c in checksum):
            raise ValueError('Invalid checksum')


def verify(root, skill_root=None):
    root = Path(root).absolute()
    actual = inventory(root)
    manifest = json.loads((root / 'DISTRIBUTION_MANIFEST.json').read_bytes(), object_pairs_hook=unique_object)
    if manifest['schema_version'] != 1 or manifest['host'] != 'cursor' or manifest['status'] != 'pending-real-host-acceptance':
        raise ValueError('Unexpected candidate identity')
    check_paths(manifest['files'])
    actual.pop('DISTRIBUTION_MANIFEST.json')
    if actual != manifest['files']:
        raise ValueError('Distribution has missing, extra or changed files')
    host = json.loads((root / 'HOST_MANIFEST.json').read_bytes(), object_pairs_hook=unique_object)
    if host['host'] != 'cursor' or host['release'] != manifest['candidate']:
        raise ValueError('Host manifest disagrees with distribution')
    check_paths(host['files'])
    if inventory(root / 'tie-studio') != host['files']:
        raise ValueError('Host payload mismatch')
    if skill_root is not None and inventory(Path(skill_root).absolute()) != host['files']:
        raise ValueError('Installed Skill has missing, extra or changed files')
    return {'candidate': manifest['candidate'], 'source_commit': manifest['source']['commit'],
            'payload_files': len(host['files']), 'status': manifest['status'],
            'installed_copy_verified': skill_root is not None}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skill-root', type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(Path(__file__).absolute().parent, args.skill_root), indent=2))

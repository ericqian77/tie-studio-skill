#!/usr/bin/env python3
"""Validate host-authored source projections and render an offline TIE workbench.

No semantic extraction, model calls or source edits. Python 3.9+.
Optional local lifecycle commands live in tie_dashboard_server.py.
The dependency-free schema checker intentionally implements only the keywords used
in the bundled private schema; unsupported schema keywords fail closed.
"""
import argparse
from datetime import datetime, timezone
import hashlib
from html import escape
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
import tempfile

ASSETS = Path(__file__).resolve().parents[1] / 'assets' / 'dashboard'
MAX_BYTES = 8 * 1024 * 1024
SUPPORTED_LOCALES = ('en', 'zh-CN')


class ProjectionError(ValueError):
    pass


def read_bytes(path):
    with path.open('rb') as handle:
        data = handle.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ProjectionError('Input exceeds the 8 MiB limit: ' + str(path))
    return data


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ProjectionError('Duplicate JSON key: ' + key)
        result[key] = value
    return result


def load_json(path):
    return json.loads(read_bytes(path).decode('utf-8'), object_pairs_hook=unique_object)


def load_messages(locale):
    # Locale identifiers never become unchecked paths. A partial translation must not
    # silently leave source/authority or freshness labels in another language.
    if locale not in SUPPORTED_LOCALES:
        raise ProjectionError('Unsupported UI locale: ' + str(locale))
    english = load_json(ASSETS / 'locales' / 'en.json')
    messages = english if locale == 'en' else load_json(ASSETS / 'locales' / (locale + '.json'))
    if (not isinstance(messages, dict) or set(messages) != set(english) or
            any(not isinstance(v, str) or not v.strip() for v in messages.values())):
        raise ProjectionError('Incomplete UI locale resource: ' + locale)
    return messages


def check_schema(value, schema, at='$'):
    allowed = {'$schema', '$id', 'title', 'type', 'const', 'enum', 'minLength', 'pattern',
               'minimum', 'properties', 'required', 'additionalProperties', 'items', 'minItems', 'anyOf'}
    if set(schema) - allowed:
        raise ProjectionError('Unsupported internal schema keyword')
    if 'anyOf' in schema:
        for option in schema['anyOf']:
            try:
                check_schema(value, option, at)
                return
            except ProjectionError:
                pass
        raise ProjectionError(at + ': no allowed shape matches')
    types = {'object': dict, 'array': list, 'string': str, 'integer': int, 'null': type(None)}
    if 'type' in schema and type(value) is not types[schema['type']]:
        raise ProjectionError(at + ': expected ' + schema['type'])
    if 'const' in schema and (type(value) is not type(schema['const']) or value != schema['const']):
        raise ProjectionError(at + ': unexpected constant')
    if 'enum' in schema and value not in schema['enum']:
        raise ProjectionError(at + ': invalid machine identifier')
    if isinstance(value, str):
        if len(value.strip()) < schema.get('minLength', 0):
            raise ProjectionError(at + ': empty text')
        if 'pattern' in schema and not re.fullmatch(schema['pattern'], value):
            raise ProjectionError(at + ': invalid format')
    if type(value) is int and value < schema.get('minimum', value):
        raise ProjectionError(at + ': below minimum')
    if isinstance(value, dict):
        props = schema.get('properties', {})
        if set(schema.get('required', [])) - set(value):
            raise ProjectionError(at + ': missing required fields')
        if schema.get('additionalProperties') is False and set(value) - set(props):
            raise ProjectionError(at + ': unknown fields')
        for key, item in value.items():
            if key in props:
                check_schema(item, props[key], at + '.' + key)
    if isinstance(value, list):
        if len(value) < schema.get('minItems', 0):
            raise ProjectionError(at + ': too few items')
        for i, item in enumerate(value):
            check_schema(item, schema['items'], at + '[' + str(i) + ']')


def index_unique(items, name):
    result = {}
    for item in items:
        if item['id'] in result:
            raise ProjectionError(name + ': duplicate ID ' + item['id'])
        result[item['id']] = item
    return result


def source_path(root, relative):
    path = PurePosixPath(relative)
    if path.is_absolute() or '..' in path.parts or '\\' in relative or ':' in relative or str(path) != relative:
        raise ProjectionError('Source path must be a normalized project-relative path: ' + relative)
    resolved = (root / relative).resolve()
    if not resolved.is_relative_to(root):
        raise ProjectionError('Source escapes the selected project: ' + relative)
    if not resolved.is_file():
        raise ProjectionError('Source is missing or is not a file: ' + relative)
    return resolved


def validate(view, project):
    """Check structure, references, exact excerpts and complete-file fingerprints."""
    root = Path(project).resolve(strict=True)
    check_schema(view, load_json(ASSETS / 'view.schema.json'))
    load_messages(view['uiLocale'])
    try:
        stamp = datetime.fromisoformat(view['generatedAt'].replace('Z', '+00:00'))
        if stamp.tzinfo is None:
            raise ValueError('timezone missing')
    except ValueError as error:
        raise ProjectionError('generatedAt must be an ISO timestamp with timezone') from error
    src = index_unique(view['sources'], 'sources')
    refs = index_unique(view['citations'], 'citations')
    records = index_unique(view['records'], 'records')
    index_unique(view['events'], 'events')
    paths, lines = {}, {}
    for key, source in src.items():
        path = source_path(root, source['path'])
        if path in paths.values():
            raise ProjectionError('Duplicate resolved source path')
        data = read_bytes(path)
        if hashlib.sha256(data).hexdigest() != source['sha256']:
            raise ProjectionError('Stale source: ' + source['path'])
        paths[key] = path
        lines[key] = data.decode('utf-8').splitlines()
    for ref in refs.values():
        if ref['source'] not in src:
            raise ProjectionError('Citation has an unknown source: ' + ref['id'])
        text = lines[ref['source']]
        if ref['end'] < ref['start'] or ref['end'] > len(text):
            raise ProjectionError('Citation line range is invalid: ' + ref['id'])
        if '\n'.join(text[ref['start']-1:ref['end']]) != ref['excerpt']:
            raise ProjectionError('Citation excerpt differs from source: ' + ref['id'])

    def check_refs(ids):
        if len(ids) != len(set(ids)) or any(key not in refs for key in ids):
            raise ProjectionError('Unknown or repeated citation reference')

    for record in records.values():
        check_refs(record['citations'])
    for relation in view['relations']:
        if relation['from'] not in records or relation['to'] not in records or relation['from'] == relation['to']:
            raise ProjectionError('Invalid relation endpoint')
        if relation['basis'] == 'source' and not relation['citations']:
            raise ProjectionError('Source-recorded relation requires a citation')
        check_refs(relation['citations'])
    for event in view['events']:
        if len(event['records']) != len(set(event['records'])) or any(key not in records for key in event['records']):
            raise ProjectionError('Invalid event record reference')
        check_refs(event['citations'])
        check_refs(event['after']['citations'])
        if event['before'] is not None:
            check_refs(event['before']['citations'])
    # Detect a change during validation, including after excerpts were read.
    for key, path in paths.items():
        if source_path(root, src[key]['path']) != path or hashlib.sha256(read_bytes(path)).hexdigest() != src[key]['sha256']:
            raise ProjectionError('Source changed during validation: ' + src[key]['path'])
    return root


def safe_json(value):
    # Embedded application/json must not be able to terminate its script element.
    return json.dumps(value, ensure_ascii=False, allow_nan=False).replace('&', '\\u0026').replace('<', '\\u003c').replace('>', '\\u003e').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')


def build_html(view, build):
    messages = load_messages(view['uiLocale'])
    payload = {'view': view, 'messages': messages, 'build': build}
    template = (ASSETS / 'index.html').read_text(encoding='utf-8')
    replacements = {'/*__LANG__*/': escape(view['uiLocale'], quote=True),
                    '/*__SKIP__*/': escape(messages['skip']),
                    '/*__NAV__*/': escape(messages['navLabel'], quote=True),
                    '/*__DETAIL__*/': escape(messages['detail'], quote=True),
                    '/*__NOSCRIPT__*/': escape(messages['noJavaScript']),
                    '/*__STYLE__*/': (ASSETS / 'dashboard.css').read_text(encoding='utf-8'),
                    '/*__PAYLOAD__*/': safe_json(payload),
                    '/*__SCRIPT__*/': (ASSETS / 'dashboard.js').read_text(encoding='utf-8')}
    for marker in replacements:
        if template.count(marker) != 1:
            raise ProjectionError('Invalid internal template marker: ' + marker)
    if build['kind'] == 'live':
        template = template.replace("connect-src 'none'", "connect-src 'self'")
        replacements['/*__SCRIPT__*/'] = (ASSETS / 'dashboard-live.js').read_text(encoding='utf-8') + '\n' + replacements['/*__SCRIPT__*/']
    # One pass: source text containing a template marker remains literal content.
    html = re.sub(r'/\*__[A-Z]+__\*/', lambda m: replacements[m.group()], template)
    return html


def render(view, project, output):
    root = validate(view, project)
    destination = Path(output).absolute()
    if destination.suffix.lower() != '.html' or destination.is_symlink():
        raise ProjectionError('Output must be a non-symlink .html file')
    resolved = destination.resolve()
    skill_root = ASSETS.parents[1]
    if resolved.is_relative_to(skill_root) or any(resolved == source_path(root, s['path']) for s in view['sources']):
        raise ProjectionError('Output must not overwrite Skill assets or source evidence')
    if destination.exists() and b'id="tie-payload"' not in read_bytes(destination):
        raise ProjectionError('Refusing to overwrite a file that is not a generated dashboard')
    html = build_html(view, {'kind':'static', 'projectRoot':str(root),
                             'checkedAt':datetime.now(timezone.utc).isoformat(timespec='seconds')})
    validate(view, root)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temp = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=destination.parent, suffix='.tmp', delete=False) as handle:
            temp = Path(handle.name)
            handle.write(html)
            handle.flush()
            os.fsync(handle.fileno())
        # Do not publish an output assembled across different source revisions.
        validate(view, root)
        os.replace(temp, destination)
    finally:
        if temp and temp.exists():
            temp.unlink()
    return destination


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('validate', 'render'):
        cmd = sub.add_parser(name, help='Check a projection' if name == 'validate' else 'Write a self-contained static HTML snapshot')
        cmd.add_argument('--view', type=Path, required=True, help='Host-authored view.json')
        cmd.add_argument('--project', type=Path, required=True, help='Explicit source workspace root')
        if name == 'render':
            cmd.add_argument('--output', type=Path, required=True, help='Output .html path outside the Skill source')
    from tie_dashboard_server import add_commands, run_command
    add_commands(sub)
    args = parser.parse_args(argv)
    try:
        if args.command not in {'validate', 'render'}:
            return run_command(args)
        view = load_json(args.view)
        if args.command == 'validate':
            validate(view, args.project)
            print('OK: projection structure, references, excerpts and source fingerprints (not semantic approval)')
        else:
            result = render(view, args.project, args.output)
            print('OK: static snapshot written to ' + str(result))
        return 0
    except (ProjectionError, OSError, UnicodeError, ValueError, RecursionError) as error:
        print('ERROR: ' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())

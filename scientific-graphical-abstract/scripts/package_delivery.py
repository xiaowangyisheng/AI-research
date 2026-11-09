#!/usr/bin/env python3
"""Package only explicitly listed delivery files with checksums; no overwrites."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys
import zipfile

def package(root, manifest_path, output):
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError('Root must be a directory')
    output = Path(output).absolute()
    manifest = json.loads(Path(manifest_path).read_text(encoding='utf-8'))
    if not isinstance(manifest, dict) or not isinstance(manifest.get('files'), list) or not manifest['files']:
        raise ValueError('Manifest must contain a non-empty files list')
    if 'required_roles' not in manifest or not isinstance(manifest['required_roles'], list):
        raise ValueError('Specify required_roles explicitly according to task scope')
    if any(not isinstance(r, str) or not r for r in manifest['required_roles']):
        raise ValueError('required_roles must contain non-empty strings')
    seen, roles, files = set(), set(), []
    for entry in manifest['files']:
        if not isinstance(entry, dict):
            raise ValueError('Each file entry must be an object')
        relative, role = entry.get('path'), entry.get('role')
        if not isinstance(relative, str) or not relative or not isinstance(role, str) or not role:
            raise ValueError('Each file needs path and role strings')
        p = PurePosixPath(relative)
        if p.is_absolute() or '..' in p.parts or '\\' in relative or ':' in relative:
            raise ValueError(f'Unsafe archive path: {relative}')
        normalized = p.as_posix()
        if normalized == 'delivery_manifest.json' or normalized in seen:
            raise ValueError(f'Duplicate/reserved archive path: {normalized}')
        seen.add(normalized)
        resolved = (root / normalized).resolve(strict=True)
        if root not in resolved.parents:
            raise ValueError(f'File escapes package root: {relative}')
        if not resolved.is_file() or resolved.stat().st_size == 0:
            raise ValueError(f'Missing or empty file: {relative}')
        if resolved == output.resolve():
            raise ValueError('Output archive cannot also be an input')
        roles.add(role)
        files.append((entry, normalized, resolved))
    missing = set(manifest['required_roles']) - roles
    if missing:
        raise ValueError('Missing required roles: ' + ', '.join(sorted(missing)))
    # Snapshot input bytes before creating the archive. This also gives checksums
    # of exactly what is packaged rather than of a file that may later change.
    contents = []
    enriched = []
    for entry, name, source in files:
        blob = source.read_bytes()
        contents.append((name, blob))
        enriched.append(dict(entry, path=name, bytes=len(blob), sha256=hashlib.sha256(blob).hexdigest()))
    manifest = dict(manifest, files=enriched)
    encoded = json.dumps(manifest, ensure_ascii=False, indent=2).encode('utf-8')
    # Parent directory must already exist; no surprise directory creation.
    with zipfile.ZipFile(output, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for name, blob in contents:
            archive.writestr(name, blob)
        archive.writestr('delivery_manifest.json', encoded)
    with zipfile.ZipFile(output) as archive:
        failure = archive.testzip()
        if failure:
            raise ValueError(f'Archive integrity failed: {failure}')
    return {'archive': str(output), 'files': len(contents), 'roles': sorted(roles),
            'bytes': output.stat().st_size, 'zip_integrity_pass': True}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True, type=Path)
    parser.add_argument('--manifest', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(package(args.root, args.manifest, args.output), ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        print(f'Packaging failed: {exc}', file=sys.stderr)
        return 2

if __name__ == '__main__':
    sys.exit(main())

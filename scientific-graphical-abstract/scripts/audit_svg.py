#!/usr/bin/env python3
"""Read-only SVG structure audit; not a visual or Illustrator compatibility test."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

GRAPHICS = {'path', 'rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon'}

def audit(path, expect='vector', require_text=False):
    data = Path(path).read_bytes()
    # Do not resolve XML entities or accept arbitrary executable documents.
    if b'<!ENTITY' in data.upper():
        raise ValueError('XML entity declarations are not supported')
    root = ET.fromstring(data)
    if root.tag.split('}')[-1] != 'svg':
        raise ValueError('Root element is not SVG')
    counts = Counter()
    ids = Counter()
    external = set()
    local_refs = set()
    fonts = set()
    event_attributes = []
    images = {'data_uri': 0, 'external': 0, 'internal_reference': 0, 'missing_href': 0}
    texts = []
    for node in root.iter():
        tag = node.tag.split('}')[-1]
        counts[tag] += 1
        if node.get('id'):
            ids[node.get('id')] += 1
        style = node.get('style', '')
        if node.get('font-family'):
            fonts.add(node.get('font-family'))
        fonts.update(re.findall(r'font-family\s*:\s*([^;}]+)', style))
        if tag == 'style':
            style += node.text or ''
            fonts.update(re.findall(r'font-family\s*:\s*([^;}]+)', style))
        href = node.get('href') or node.get('{http://www.w3.org/1999/xlink}href')
        if href:
            if href.startswith('#'):
                local_refs.add(href[1:])
            elif not href.startswith('data:'):
                external.add(href)
        if tag == 'image':
            kind = 'missing_href' if not href else 'data_uri' if href.startswith('data:') else 'internal_reference' if href.startswith('#') else 'external'
            images[kind] += 1
        if tag == 'text':
            texts.append(''.join(node.itertext()))
        for key, value in node.attrib.items():
            if key.split('}')[-1].lower().startswith('on'):
                event_attributes.append(key)
            for ref in re.findall(r'url\(\s*[\'"]?([^\)\'"\s]+)', value):
                if ref.startswith('#'):
                    local_refs.add(ref[1:])
                elif not ref.startswith('data:'):
                    external.add(ref)
        for ref in re.findall(r'url\(\s*[\'"]?([^\)\'"\s]+)', style):
            if ref.startswith('#'):
                local_refs.add(ref[1:])
            elif not ref.startswith('data:'):
                external.add(ref)
        if '@import' in style.lower():
            external.add('CSS @import present; inspect manually')
    errors = []
    warnings = []
    if expect == 'vector' and counts['image']:
        errors.append('Full-vector expectation violated: image elements present')
    if require_text and not any(t.strip() for t in texts):
        errors.append('No non-empty native text elements')
    if counts['script'] or counts['foreignObject'] or event_attributes:
        errors.append('Executable/foreign content or event attributes require manual removal/review')
    if external:
        errors.append('External dependencies present; make delivery self-contained')
    duplicate = sorted(k for k, v in ids.items() if v > 1)
    if duplicate:
        errors.append('Duplicate SVG IDs')
    missing = sorted(local_refs - set(ids))
    if missing:
        errors.append('Unresolved internal references')
    if images['missing_href']:
        errors.append('Image element without href')
    if counts['filter']:
        warnings.append('SVG filters may differ in Illustrator; native application check recommended')
    if counts['use']:
        warnings.append('Referenced symbols/use elements: inspect editability after opening')
    if not texts:
        warnings.append('Text may be outlined, rasterized, or absent; do not claim editable labels')
    return {
        'file': Path(path).name, 'bytes': len(data), 'expectation': expect,
        'width': root.get('width'), 'height': root.get('height'), 'viewBox': root.get('viewBox'),
        'native_text_elements': counts['text'], 'image_elements': counts['image'],
        'image_types': images, 'graphic_elements': sum(counts[k] for k in GRAPHICS),
        'paths': counts['path'], 'groups': counts['g'], 'fonts': sorted(fonts),
        'duplicate_ids': duplicate, 'unresolved_internal_ids': missing,
        'external_dependencies': sorted(external), 'errors': errors, 'warnings': warnings,
        'structural_pass': not errors, 'visual_review_required': True,
        'illustrator_tested': False,
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('svg', type=Path)
    parser.add_argument('--expect', choices=['vector', 'hybrid'], default='vector')
    parser.add_argument('--require-text', action='store_true')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        report = audit(args.svg, args.expect, args.require_text)
        encoded = json.dumps(report, ensure_ascii=False, indent=2)
        if args.output:
            # Do not overwrite earlier QA or a source file accidentally.
            with args.output.open('x', encoding='utf-8') as handle:
                handle.write(encoded + '\n')
        print(encoded)
        return 0 if report['structural_pass'] else 2
    except (OSError, ValueError, ET.ParseError) as exc:
        print(f'Audit failed: {exc}', file=sys.stderr)
        return 2

if __name__ == '__main__':
    sys.exit(main())

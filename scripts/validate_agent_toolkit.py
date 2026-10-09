#!/usr/bin/env python3
"""Validate repository toolkit structure; this does not evaluate agent behavior."""
from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote

import yaml

BASELINE = frozenset('build investigate research verify review fix release deploy publish push pull'.split())
# Claude Code loads these adapters only on an explicit /name invocation.
CLAUDE_USER_ONLY = frozenset('release deploy publish'.split())
CLAUDE_GATE = {'disable-model-invocation': True}
CONTRACTS = frozenset('core authorization verification git-github deployment handoff memory scopes'.split())
REQUIRED = (
    ['AGENTS.md', 'CLAUDE.md', '.agent/README.md', '.agent/project.yaml',
     '.agent/integrations/README.md', '.agent/workflows/README.md',
     '.agent/hooks/README.md', '.agent/evals/skill-routing.md']
    + [f'.agent/contracts/{name}.md' for name in sorted(CONTRACTS)]
)


class Invalid(ValueError):
    pass


class UniqueLoader(yaml.SafeLoader):
    """Reject duplicate keys instead of silently replacing earlier policy data."""


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise Invalid(f'duplicate YAML key: {key}')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def require(condition, message):
    if not condition:
        raise Invalid(message)


def mapping(path):
    result = yaml.load(path.read_text(), Loader=UniqueLoader)
    require(isinstance(result, dict), f'{path}: expected mapping')
    return result


def frontmatter(path, provider_fields=None):
    provider_fields = provider_fields or {}
    raw = path.read_text()
    require(raw.startswith('---\n'), f'{path}: missing frontmatter')
    parts = raw.split('---\n', 2)
    require(len(parts) == 3, f'{path}: unclosed frontmatter')
    data = yaml.load(parts[1], Loader=UniqueLoader)
    if provider_fields:
        require(isinstance(data, dict) and set(data) == {'name', 'description'} | set(provider_fields),
                f'{path}: expected name/description plus {", ".join(provider_fields)}')
        for key, value in provider_fields.items():
            require(data[key] is value, f'{path}: {key} must be {value!r}')
        data = {key: value for key, value in data.items() if key not in provider_fields}
    require(isinstance(data, dict) and set(data) == {'name', 'description'},
            f'{path}: expected portable name/description')
    require(data['name'] == path.parent.name, f'{path}: name differs from directory')
    require(re.fullmatch(r'[a-z][a-z0-9-]{0,63}', data['name']), f'{path}: invalid name')
    require(isinstance(data['description'], str) and 10 <= len(data['description']) <= 1024,
            f'{path}: invalid description')
    return data


def adapter_text(name, description, canonical, gated=False):
    gate = 'disable-model-invocation: true\n' if gated else ''
    return (
        f'---\nname: {name}\ndescription: {description}\n{gate}---\n\n'
        f'Read and follow `{canonical}` from the repository root before acting.\n'
        'Also follow `AGENTS.md` and applicable scoped instructions.\n'
        'This is a discovery adapter only; canonical workflow policy lives in `skills/`.\n'
    )


def validate(root):
    root = root.resolve()
    for rel in REQUIRED:
        require((root / rel).is_file(), f'missing {rel}')
    project = mapping(root / '.agent/project.yaml')
    require(project['schema_version'] == 1, 'unsupported project schema')
    repo = project['repository']
    require(repo == dict(host='github', owner='mind-seed-systems', name='.github',
                         default_branch='main', canonical_remote='origin'), 'repository identity drift')
    identity = 'github:mind-seed-systems/.github'
    require(project['project']['id'] == identity, 'project identity drift')
    require(project['organization'] == {'id': 'github:mind-seed-systems', 'name': 'Mind Seed Systems'},
            'organization identity drift')
    require(project['ownership']['class'] == 'user-owned', 'ownership classification drift')
    require(project['agent'] == dict(instructions='AGENTS.md', canonical_skills='skills/',
                                    project_specific_skills='skills/project/'), 'agent discovery drift')
    require(project['mind_seed'] == dict(enabled=True, binding='.mind-seed/project.yaml'),
            'Mind-Seed discovery drift')
    for rel in project['environment']['source_files']:
        require((root / rel).is_file(), f'missing environment source {rel}')
    # These are intentionally public, unconnected bindings. Adoption of a real
    # backend needs a reviewed contract/validator change, not just a flipped flag.
    bindings = {name: mapping(root / f'.mind-seed/{name}.yaml') for name in
                ('project', 'relationships', 'scopes', 'memory', 'integrations')}
    for name, value in bindings.items():
        require(value['schema_version'] == 1, f'{name}: unsupported schema')
        if name != 'integrations':
            require(value['project_id'] == identity, f'{name}: project identity mismatch')
    bound = bindings['project']
    require(bound['organization_id'] == project['organization']['id'], 'binding organization mismatch')
    require(bound['registry'] == dict(enabled=False, canonical=False, project_id=None,
                                     organization_id=None, reconciliation='unresolved-no-configured-public-endpoint'),
            'unverified registry binding')
    for name, target in [('repository', '../.agent/project.yaml'), ('relationships', 'relationships.yaml'),
                         ('scopes', 'scopes.yaml'), ('memory', 'memory.yaml'), ('integrations', 'integrations.yaml')]:
        require(bound[name]['binding'] == target and (root / '.mind-seed' / target).is_file(),
                f'{name}: broken binding')
    require(bindings['relationships']['relationships'] == [dict(type='belongs-to',
                target_id='github:mind-seed-systems', authority='repository')], 'unverified relationship')
    scope = bindings['scopes']['bindings']
    require(set(scope) == {'global', 'organization', 'project', 'repository', 'agent', 'task', 'session'},
            'scope coverage mismatch')
    for name in ('global', 'organization', 'project', 'repository'):
        require(scope[name] == {'id': None}, f'{name}: unverified external scope')
    for name in ('agent', 'task', 'session'):
        require(scope[name] == {'dynamic': True}, f'{name}: must remain dynamic')
    memory = bindings['memory']
    require(memory['enabled'] is False and memory['backend'] is None, 'unverified memory backend')
    require(memory['permissions'] == {'read': [], 'write': []}, 'ungranted memory permissions')
    require(memory['mutation'] == {'authority': 'none', 'promotion_requires_authority': True},
            'ungranted memory mutation')
    require(memory['scopes'] == dict(organization=None, project=None, repository=None),
            'unverified memory scopes')
    for key, target in [('authority_contract', '../.agent/contracts/memory.md'),
                        ('scope_contract', '../.agent/contracts/scopes.md')]:
        require(memory[key] == target and (root / '.mind-seed' / target).is_file(), 'broken memory contract')
    require(bindings['integrations']['integrations'] == {'github': {
        'enabled': True, 'repository': 'mind-seed-systems/.github',
        'configuration': '../.agent/integrations/README.md'}}, 'unverified integration')
    require((root / 'CLAUDE.md').read_text() == '@AGENTS.md\n', 'Claude instruction fork')
    require((root / '.codex/skills').is_symlink() and
            (root / '.codex/skills').resolve() == root / '.agents/skills', 'Codex compatibility link drift')
    skills = list((root / 'skills').glob('*/SKILL.md')) + list((root / 'skills/project').glob('*/SKILL.md'))
    names, descriptions = set(), set()
    for path in skills:
        data = frontmatter(path)
        name = data['name']
        require(name not in names, f'duplicate skill {name}')
        require(data['description'] not in descriptions, f'indistinct description: {name}')
        names.add(name)
        descriptions.add(data['description'])
        for provider in ('.agents', '.claude'):
            adapter = root / provider / 'skills' / name / 'SKILL.md'
            gated = provider == '.claude' and name in CLAUDE_USER_ONLY
            require(adapter.is_file(), f'missing {adapter}')
            require(frontmatter(adapter, CLAUDE_GATE if gated else None) == data, f'{adapter}: metadata drift')
            require(adapter.read_text() == adapter_text(name, data['description'], path.relative_to(root).as_posix(),
                                                        gated),
                    f'{adapter}: adapter policy drift')
    require(BASELINE <= names, 'missing baseline skill')
    for provider in ('.agents', '.claude'):
        found = {p.parent.name for p in (root / provider / 'skills').glob('*/SKILL.md')}
        require(found == names, f'{provider}: orphan adapters')
    routing = (root / '.agent/evals/skill-routing.md').read_text()
    for name in names:
        match = re.search(rf'^## {re.escape(name)}\n(.*?)(?=^## |\Z)', routing, re.M | re.S)
        require(match, f'missing routing cases for {name}')
        positive = re.findall(r'^\| positive \| .+? \| (\S+) \|$', match[1], re.M)
        negative = re.findall(r'^\| negative \| .+? \| (\S+) \|$', match[1], re.M)
        require(len(positive) >= 3 and all(n == name for n in positive), f'{name}: invalid positive cases')
        require(len(negative) >= 2 and all(n in names and n != name for n in negative),
                f'{name}: invalid negative cases')
    markdown = [root / p for p in ('AGENTS.md', 'CLAUDE.md', 'README.md')]
    for folder in ('.agent', 'skills', '.agents', '.claude'):
        markdown.extend((root / folder).rglob('*.md'))
    for path in markdown:
        for link in re.findall(r'\[[^\]]+\]\(([^)]+)\)', path.read_text()):
            if re.match(r'[a-z]+:', link) or link.startswith('#'):
                continue
            target = (path.parent / unquote(link.split('#', 1)[0])).resolve()
            require(target.is_relative_to(root) and target.exists(), f'{path}: broken local link {link}')
    return len(skills)


def main():
    root = Path(__file__).resolve().parents[1]
    try:
        count = validate(root)
        paths = subprocess.check_output(['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'],
                                        cwd=root).decode().split('\0')
        for rel in filter(None, paths):
            path = root / rel
            if path.suffix == '.json':
                json.loads(path.read_text())
            elif path.suffix in ('.yaml', '.yml'):
                mapping(path)
        print(f'Toolkit structure passed: {count} canonical skills; bindings, adapters, links and routing coverage valid.')
        print('Repository JSON/YAML parsed. Behavioral routing and provider discovery require separate evidence.')
    except (Invalid, KeyError, TypeError, OSError, yaml.YAMLError, json.JSONDecodeError) as exc:
        print(f'Toolkit validation failed: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())

"""Focused regressions for schema, semantic identity, paths, and opt-in reads."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import validate_organization as validator


class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads(validator.MANIFEST_PATH.read_text())

    def fails(self, change, message):
        change(self.manifest)
        with self.assertRaisesRegex(validator.ValidationError, message):
            validator.validate_manifest(self.manifest)

    def test_current_three_repositories_pass(self):
        self.assertEqual(validator.validate_manifest(self.manifest), (3, 13, 5))

    def test_inventory_is_not_hard_coded(self):
        repository = copy.deepcopy(self.manifest['repositories'][-1])
        repository.update(id='test-component', name='mind-seed-test', role='component',
                          url='https://github.com/mind-seed-systems/mind-seed-test')
        repository['documentation'] = [{'repository': 'mind-seed-test', 'path': 'README.md'}]
        self.manifest['repositories'].append(repository)
        self.assertEqual(validator.validate_manifest(self.manifest)[0], 4)

    def test_invalid_lifecycle(self):
        self.fails(lambda m: m['repositories'][0].update(lifecycle='invalid'), 'JSON Schema')

    def test_invalid_relationship_status(self):
        self.fails(lambda m: m['relationships'][0].update(status='invalid'), 'JSON Schema')

    def test_required_fields(self):
        for field in ('organization', 'authorities', 'relationships'):
            with self.subTest(field=field):
                candidate = copy.deepcopy(self.manifest)
                del candidate[field]
                with self.assertRaisesRegex(validator.ValidationError, 'JSON Schema'):
                    validator.validate_manifest(candidate)

    def test_missing_repository_field(self):
        self.fails(lambda m: m['repositories'][0].pop('releaseStatus'), 'JSON Schema')

    def test_unknown_properties(self):
        self.fails(lambda m: m.update(unexpected=True), 'JSON Schema')

    def test_unknown_nested_properties(self):
        self.fails(lambda m: m['repositories'][0].update(unexpected=True), 'JSON Schema')

    def test_unknown_relationship_reference(self):
        self.fails(lambda m: m['relationships'][0].update(target='unknown'), 'unknown target')

    def test_unknown_component_owner(self):
        self.fails(lambda m: m['componentDomains'][0].update(currentOwner='unknown'), 'unknown owner')

    def test_unknown_documentation_repository(self):
        self.fails(lambda m: m['repositories'][0]['documentation'][0].update(repository='unknown'), 'unknown documentation')

    def test_repository_identity(self):
        self.fails(lambda m: m['repositories'][0].update(url='https://github.com/other/.github'), 'identity')

    def test_required_core_and_infrastructure(self):
        for role in ('canonical-core', 'organization-infrastructure'):
            with self.subTest(role=role):
                candidate = copy.deepcopy(self.manifest)
                next(r for r in candidate['repositories'] if r['role'] == role)['role'] = 'infrastructure'
                with self.assertRaises(validator.ValidationError):
                    validator.validate_manifest(candidate)

    def test_broken_evidence_fragment(self):
        self.fails(lambda m: m['relationships'][0].update(evidence='docs/organization-architecture.md#missing-heading'), 'unknown Markdown fragment')

    def test_documentation_fragment(self):
        self.fails(lambda m: m['repositories'][0]['documentation'][0].update(path='README.md#missing-heading'), 'unknown Markdown fragment')

    def test_unsafe_references_including_private_paths(self):
        for path in ('../README.md', '/README.md', '%2e%2e/README.md', 'docs/../../README.md',
                     'https://example.com/README.md', 'docs\\README.md', 'docs//README.md',
                     'README.md?query=1', 'docs/%00file.md'):
            with self.subTest(path=path):
                with self.assertRaisesRegex(validator.ValidationError, 'unsafe'):
                    validator.validate_reference(path, local=False)

    def test_symlink_escape(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'repo'
            root.mkdir()
            (Path(tmp) / 'outside.md').write_text('# Outside\n')
            (root / 'escape.md').symlink_to(Path(tmp) / 'outside.md')
            with patch.object(validator, 'ROOT', root):
                with self.assertRaisesRegex(validator.ValidationError, 'escapes'):
                    validator.validate_reference('escape.md', local=True)

    def test_heading_duplicates_and_fences(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'README.md'
            path.write_text('# Same\n# Same\n```md\n# Hidden\n```\n## `Code` & words\n')
            self.assertEqual(validator.markdown_fragments(path), {'same', 'same-1', 'code--words'})

    def test_live_reads_only(self):
        live = [{'name': r['name'], 'visibility': r['visibility'], 'default_branch': r['defaultBranch']}
                for r in self.manifest['repositories']]
        with patch.object(validator.subprocess, 'run', side_effect=[
                subprocess.CompletedProcess([], 0), subprocess.CompletedProcess([], 0, json.dumps([live]))]) as run:
            validator.validate_live_inventory(self.manifest)
        command = run.call_args_list[1].args[0]
        self.assertEqual(command[command.index('--method') + 1], 'GET')

    def test_missing_live_access_fails(self):
        with patch.object(validator.subprocess, 'run', side_effect=FileNotFoundError):
            with self.assertRaisesRegex(validator.ValidationError, 'authenticated gh'):
                validator.validate_live_inventory(self.manifest)

    def test_incomplete_live_inventory_fails(self):
        with patch.object(validator.subprocess, 'run', side_effect=[
                subprocess.CompletedProcess([], 0), subprocess.CompletedProcess([], 0, '[]')]):
            with self.assertRaisesRegex(validator.ValidationError, 'incomplete private-repository access'):
                validator.validate_live_inventory(self.manifest)

    def test_offline_validation_never_calls_gh(self):
        with patch.object(validator.subprocess, 'run', side_effect=AssertionError('unexpected network')):
            validator.validate_manifest(self.manifest)


if __name__ == '__main__':
    unittest.main()

"""Execute the actual workflow shell bodies against small synthetic histories."""
import os
from pathlib import Path
import subprocess
import tempfile
import textwrap
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = (ROOT / '.github/workflows/validate-organization-foundation.yml',
             ROOT / 'workflow-templates/repository-hygiene.yml')


def whitespace_script(path):
    step = path.read_text().split('      - name: Check patch whitespace\n', 1)[1]
    body = step.split('        run: |\n', 1)[1].split('\n      - name:', 1)[0]
    return textwrap.dedent(body)


class WhitespaceTests(unittest.TestCase):
    def test_committed_change_event_ranges(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            def git(*args):
                return subprocess.check_output(['git', *args], cwd=root, stderr=subprocess.DEVNULL, text=True).strip()
            git('init', '-b', 'main')
            git('config', 'user.name', 'Test')
            git('config', 'user.email', 'test@example.invalid')
            (root / 'sample.txt').write_text('clean\n')
            git('add', 'sample.txt')
            git('commit', '-m', 'base')
            base = git('rev-parse', 'HEAD')
            (root / 'sample.txt').write_text('bad whitespace \n')
            git('add', 'sample.txt')
            git('commit', '-m', 'bad whitespace')
            head = git('rev-parse', 'HEAD')
            self.assertEqual(git('status', '--porcelain'), '')
            # Prove the old clean-worktree check misses the committed defect.
            git('diff', '--check')
            for workflow in WORKFLOWS:
                for event, before in [('pull_request', ''), ('push', base),
                                      ('push', '0' * 40), ('push', ''), ('workflow_dispatch', '')]:
                    with self.subTest(workflow=workflow.name, event=event, before=before):
                        env = dict(os.environ, EVENT_NAME=event, BEFORE_SHA=before,
                                   BASE_SHA=base, HEAD_SHA=head)
                        result = subprocess.run(['bash', '-c', whitespace_script(workflow)], cwd=root,
                                                env=env, capture_output=True, text=True)
                        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                        self.assertIn('trailing whitespace', result.stdout)
                        env['HEAD_SHA'] = base
                        clean = subprocess.run(['bash', '-c', whitespace_script(workflow)], cwd=root,
                                               env=env, capture_output=True, text=True)
                        self.assertEqual(clean.returncode, 0, clean.stdout + clean.stderr)

    def test_template_and_ci_have_same_range_logic(self):
        self.assertEqual(whitespace_script(WORKFLOWS[0]), whitespace_script(WORKFLOWS[1]))


if __name__ == '__main__':
    unittest.main()

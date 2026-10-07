# Verification contract

Classify each relevant check as `passed`, `failed`, `blocked/unavailable`,
`intentionally bypassed`, or `not required`. An unrun check is never passed.
Select checks based on changed behavior and risk; repair task-caused failures
and rerun affected checks. Do not weaken acceptance to obtain a pass.

## Repository checks

Toolkit validation requires Python 3 and PyYAML from
[scripts/requirements-toolkit.txt](../../scripts/requirements-toolkit.txt).
Use an existing environment, an isolated virtual environment, or on Nix:

```sh
nix-shell -p python3Packages.pyyaml --run 'python3 scripts/validate_agent_toolkit.py'
nix-shell -p python3Packages.pyyaml --run 'python3 -m unittest discover -s tests -v'
```

For a virtual environment, install the requirements file with that environment's
Python (`python -m pip install -r scripts/requirements-toolkit.txt`). Do not mutate
a global environment. CI uses the same commands through the tracked workflow.

Run `git diff --check` on the task diff. The validator checks metadata, parsed
frontmatter, adapter consistency, local links, public binding invariants and
routing fixture coverage. Its tests exercise malformed/inconsistent fixtures.
For community metadata, also follow the public metadata workflow.

These checks do not establish model routing behavior, public disclosure approval,
GitHub acceptance, provider discovery or live rendering. Evaluate routing cases
separately, inspect actual provider discovery when available, and report absent
provider/runtime proof. A pre-existing external check failure remains failed;
it may be non-required, but never becomes passed by description.

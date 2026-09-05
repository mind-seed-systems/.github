# Mind Seed Systems organization infrastructure

This repository is the shared GitHub control surface for
[Mind Seed Systems](https://github.com/mind-seed-systems). It contains public,
non-sensitive organization metadata, contribution standards, issue forms,
pull-request guidance, workflow templates, and the canonical semantic map of
the organization's repositories: `.github` for organization governance,
`Mind-Seed` for product/core architecture, and `OS` for the operating-system
platform and build base.

Mind Seed is a local-first, OS-integrated personal AI research system. Its
long-term direction includes persistent cognition, governed memory, tools,
automation, and increasingly integrated interaction with an owner's digital
environment. Those are research and architecture goals, not claims that every
capability is implemented or operational.

## Canonical entry points

- [Organization architecture](docs/organization-architecture.md)
- [Repository standard](docs/repository-standard.md)
- [Machine-readable organization manifest](mind-seed-organization.json)
- [Manifest schema](schemas/mind-seed-organization.schema.json)
- [Contribution guide](CONTRIBUTING.md)
- [Governance and ownership](GOVERNANCE.md)
- [Security policy](SECURITY.md)
- [AI-agent contribution rules](docs/ai-agent-contributions.md)
- [Research provenance convention](docs/research-provenance.md)
- [Architecture decision records](docs/architecture/decisions/README.md)

## Repository layout

| Path | Purpose |
| --- | --- |
| `profile/README.md` | Public organization profile |
| `.github/ISSUE_TEMPLATE/` | Default issue forms for repositories without local overrides |
| `.github/pull_request_template.md` | Default pull-request template |
| `workflow-templates/` | Optional least-privilege workflow starters |
| `config/labels.json` | Canonical label definitions and repository profiles |
| `docs/` | Organization standards and architectural decisions |
| `scripts/` | Read-only validation and explicitly invoked administrative helpers |
| `schemas/` | Machine-readable contracts |

The `.github` repository is public because GitHub requires a public special
repository for organization-wide default community-health files and the
organization profile. It must therefore contain no private source, credentials,
customer data, local paths, unpublished operational evidence, or protected
project material.

## Validation

The repository's workflow and local validator are read-only. Use Python 3.13
and install the pinned validation dependencies in an isolated environment:

```text
python -m pip install -r scripts/requirements-validation.txt
python -B scripts/validate_organization.py
python -B -m unittest discover -s tests -v
git diff --check
```

The validator enforces Draft 2020-12 JSON Schema, semantic identities, safe
reference paths, local Markdown heading fragments, labels, ADR structure, and
immutable Action pins. YAML syntax is additionally parsed in GitHub Actions.
Offline validation does not access private repositories or prove live inventory.
An authorized maintainer can explicitly request authenticated, read-only GitHub
reconciliation of names, visibility, and default branches:

```text
python -B scripts/validate_organization.py --live-inventory
```

Missing access fails clearly. Passing these checks proves repository structure
and metadata consistency only; it is not evidence
that the Mind Seed runtime is built, deployed, or release-qualified.

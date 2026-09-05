# Mind Seed repository standard

This is the default for repositories owned by `mind-seed-systems`. A repository
may override it through a documented architecture decision when its artifact or
runtime requires a different contract.

## Identity and naming

- Preserve the existing canonical names `Mind-Seed`, `OS`, and `.github`.
  Future naming conventions do not require renaming these repositories.
- Name future components `mind-seed-<component>` unless a standalone product
  identity has a documented reason to differ.
- Give every repository a concise description, semantic role in the
  organization manifest, accountable owner, lifecycle state, security
  classification, and release status.
- Default to private. Public visibility requires a reviewed non-sensitive
  purpose and distribution/rights decision.

`Mind-Seed` owns product/core behavior and application-side NixOS package/service
contracts. `OS` owns the existing platform/build base, composition, host policy,
storage, recovery, and host-side prerequisites. `.github` owns organization
governance. Work stays with its substantive owner; NixOS usage alone does not
assign product code to OS.

## Required foundation

Every substantive repository has:

- `README.md` with purpose, status, architecture entrypoint, setup, verification,
  and evidence limits;
- `SECURITY.md`, `CONTRIBUTING.md`, support guidance, issue forms, and a PR
  template, inherited from `.github` when local behavior does not differ;
- architecture decisions under `docs/architecture/decisions/` or a documented
  existing equivalent;
- an appropriate license decision before public distribution;
- a changelog and Semantic Versioning policy when it releases software;
- CI that actually fits its language and artifact;
- an entry in `mind-seed-organization.json`.

## Issue forms and label provisioning

Default issue forms may be inherited from public `.github` when a repository has
no local overrides. Referenced labels must already exist in the receiving
repository; inheriting a template does not provision labels. See GitHub's
[issue-form syntax](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms).
`config/labels.json` defines `core`, organization `infrastructure`, and OS
`platform` profiles. The platform profile reuses existing common labels plus
`area:system` and `area:integration`; it creates no new taxonomy. Synchronization
is a separate explicitly authorized action through `scripts/sync-labels.ps1`.
Defining a profile is not evidence that remote labels have been applied.

## Branches and history

- Default branch: `main`.
- Trunk-based development with short-lived branches.
- Block force pushes and deletion of `main` where the GitHub plan supports it.
- Retain an organization-owner recovery path; do not require a check that cannot
  run reliably.
- Do not rewrite published shared history.
- Prefer a linear, reviewable story but preserve merges when they carry useful
  integration history.

## Commits

Use `type(optional-scope): imperative summary` when practical. Supported types
include `feat`, `fix`, `docs`, `refactor`, `test`, `research`, `build`, `ci`,
`security`, and `chore`.

Commits are coherent and do not mix unrelated local work. Generated outputs,
dependency lock changes, schemas, migrations, and evidence artifacts are
intentional and explained. No AI attribution trailer is required by default.

## Pull requests and direct changes

Pull requests are preferred for material architecture, security, migrations,
releases, and independent review. Trusted maintainers may make coherent direct
changes when risk is low and repository policy allows it. Both paths require
proportionate verification and an honest evidence report.

## Versioning and releases

- Use Semantic Versioning for independently released software.
- Preserve existing version history; do not invent a new current version during
  infrastructure work.
- Document private source releases in the owning repository. They do not imply
  a GitHub Release, public supported release, deployment, or stable support.
  OS currently uses this posture; Mind-Seed remains internal/unreleased.
- Create GitHub Release notes only when that publication is explicitly intended
  and authorized; a documented source release does not require inventing tags.
- Release notes state scope, implemented capabilities, verification level,
  limitations, migrations, and remaining operational gates.
- A tag, package build, or passing workflow is evidence only of that action; it
  is not deployment or acceptance proof.

## Documentation and decisions

- Keep canonical information in one owner and link to it instead of copying
  long sections across repositories.
- Material architecture decisions use stable ADR identifiers and supersession
  links.
- Research-backed claims use the lightweight provenance convention.
- Machine-readable files are schema-backed, minimal, UTF-8, and validated.
- Filenames and casing must work on Linux.

## Security and automation

- Use least privilege. Repository and workflow write permissions are explicit,
  narrow, and reviewed.
- Pin third-party Actions to full immutable commit SHAs.
- Keep credentials outside Git, logs, command lines, artifacts, and durable
  evidence.
- Enable free non-destructive GitHub security analysis that fits the repository.
- Do not enable paid products, external GitHub Apps, deployments, publication,
  or visibility changes without separate approval.
- Live/provider/host/GPU/long-duration workflows are opt-in and bounded; do not
  run them on ordinary validation events.

## New repository readiness checklist

Before creation, record:

- owner and purpose;
- coherent artifact and substantive initial material;
- independent lifecycle/deployment/compatibility reason;
- dependencies and organization relationships;
- source/data/credential/security classifications;
- versioning, migration, rollback, and deprecation plan;
- docs, tests, and CI strategy;
- repository name and visibility;
- manifest and ADR changes.

If these cannot be answered, keep the work in its current repository or as a
documented future boundary.

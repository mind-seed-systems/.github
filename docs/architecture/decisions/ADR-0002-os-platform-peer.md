---
id: ADR-0002
title: Recognize the existing OS platform peer
status: accepted
date: 2026-09-05
decision_owners:
  - "@jikovec"
supersedes: []
superseded_by: null
---

# Recognize the existing OS platform peer

## Context

The organization now includes the existing private OS platform/build-base
repository. The August 15 two-repository snapshot in ADR-0001 remains historical
evidence, but cannot describe the complete current organization. Current source
and authenticated inventory support three repositories and distinct product
and platform authorities.

## Decision

Mind-Seed remains canonical product/core authority for cognition, runtime,
memory contracts, agents, capabilities, approvals, APIs, and application-side
host integration and package/service behavior. OS owns NixOS composition,
platform configuration/build base, physical-host policy, host prerequisites and
placement, storage/recovery, and OS-level deployment/integration surfaces.
They are peers; NixOS package/module usage does not transfer product ownership.

The manifest adds `os-platform`, three coarse OS-owned domains, and the additive
`current-repository` boundary, retaining `mind-seed.organization/v1`. OS is a
preserved name alongside Mind-Seed and `.github`. The latter remains organization
architecture/governance authority. OS/platform architecture gains a distinct
authority without replacing core architecture authority.

Both repositories have active NixOS build dependencies, scoped to their
respective platform and application artifacts. Mind-Seed-to-OS peer integration
is planned. No deployment relationship, containment, supersession, unconditional
product dependency on OS, runtime activation, or deployment authority is asserted.
OS's documented private source release does not establish a GitHub/public
release or supported product deployment. Mind-Seed remains internal/unreleased.

Private operational details remain outside public `.github`; only high-level
ownership, repository identities, lifecycle, and relationship semantics belong
in this decision.

## Alternatives considered

- Treat OS as a future extraction: rejected because it already owns substantive
  platform source as an organization peer.
- Move all NixOS-related work into OS: rejected because Mind-Seed owns its
  application-side integration contracts.
- Assert deployed integration: rejected without direct evidence.
- Add OS-specific schema vocabulary or rename OS: unnecessary; a generic
  additive boundary and preserved name express the accepted model.

## Consequences

The organization manifest, architecture, governance, validation, and public
profile describe all three repositories. Offline validation remains independent
of private repository access. Live inventory checks are opt-in and read-only.
This governance reconciliation does not enable services or alter repository
settings, labels, Projects, security features, releases, or private source.

## Dependencies

- Existing repositories `.github`, `Mind-Seed`, and `OS`
- External NixOS platform
- [Organization architecture](../../organization-architecture.md)
- [Organization manifest](../../../mind-seed-organization.json)

## Supersession

This partially refines [ADR-0001](ADR-0001-organization-boundary.md): its
historical two-repository inventory and implicit core-otherwise infrastructure
assumption are no longer the current model. Its central organization boundary,
single canonical core, and substantive extraction criteria remain accepted.
Whole-record `supersedes`/`superseded_by` metadata is deliberately unchanged;
these reciprocal prose links express refinement without falsely obsoleting the
original decision.

## Evidence and verification

Authenticated read-only inventory and fetched main source were reviewed on
2026-09-05. The public architecture documents the resulting high-level model;
private source excerpts and operational evidence are not reproduced. Schema,
semantic, evidence-fragment, regression, YAML, and workflow validation establish
repository consistency, not deployment or operational acceptance.

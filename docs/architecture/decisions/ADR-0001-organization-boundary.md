---
id: ADR-0001
title: Use the organization as the project boundary and keep one canonical core
status: accepted
date: 2026-08-15
decision_owners:
  - "@jikovec"
supersedes: []
superseded_by: null
---

# Use the organization as the project boundary and keep one canonical core

## Context

Mind Seed is intended to evolve from one private research repository into a
system of cooperating runtimes, memory, interfaces, integrations, protocols,
infrastructure, and research artifacts. Treating the current repository as the
permanent boundary risks a monolith. Creating repositories for every possible
subsystem before substantive code exists creates empty ownership and versioning
fiction.

## Decision

`mind-seed-systems` is the canonical GitHub project boundary.
`mind-seed-systems/Mind-Seed` remains the canonical core and historical Ardor
lineage. A second repository exists now only for required organization
infrastructure: `mind-seed-systems/.github`.

A future repository is created only for a coherent independently versionable
artifact, runtime, service, interface, infrastructure layer, or knowledge
domain with substantive material and an accountable owner. Possible subsystem
names are documented as extraction candidates rather than empty repositories.

## Alternatives considered

### Keep everything in one repository indefinitely

Rejected as a permanent rule because independently deployed or versioned
artifacts may later need distinct security, compatibility, and release
boundaries.

### Create repositories for every architectural domain now

Rejected because empty placeholders create false certainty, navigation noise,
and maintenance burden without an owned artifact.

### Use a separate organization for every product surface

Rejected for now because Mind Seed's cooperating parts need one semantic and
governance boundary. Standalone product identities can be decided later.

## Consequences

- The core remains stable during the organization bootstrap; no monorepo split
  is performed.
- Repository creation requires explicit criteria, an ADR, and a manifest
  update.
- Cross-repository relationships are typed independently of GitHub membership.
- The public `.github` repository contains only sanitized organization metadata;
  private architecture evidence remains in private repositories.
- Future extraction includes interface, migration, rollback, release, and
  security work rather than only a file move.

## Dependencies

- GitHub organization `mind-seed-systems`
- Private canonical repository `mind-seed-systems/Mind-Seed`
- Public special repository `mind-seed-systems/.github`
- `mind-seed-organization.json` and its schema

## Supersession

This is the first organization-level ADR and supersedes no prior record. A
future change to the organization boundary or canonical-core role must create a
new ADR and link both directions.

Subsequent refinement (2026-09-05): [ADR-0002](ADR-0002-os-platform-peer.md)
updates the two-repository snapshot and infrastructure ownership assumption.
The organization boundary, single canonical core, and extraction criteria remain
accepted; this record is not wholly superseded.

## Evidence and verification

The accepted baseline is represented by the live GitHub repository inventory,
the organization manifest, and the repository map in
`docs/organization-architecture.md`. Runtime or release capability is outside
this decision and requires separate evidence.

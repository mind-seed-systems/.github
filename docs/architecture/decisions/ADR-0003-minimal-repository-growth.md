---
id: ADR-0003
title: Recognize Orin and separate shared service operations
status: accepted
date: 2026-09-05
decision_owners:
  - "@jikovec"
supersedes: []
superseded_by: null
---

# Recognize Orin and separate shared service operations

## Context

The owner requested a durable organization structure with only necessary new
repositories. GitHub currently exposes four repositories; the semantic manifest
still lists three. Shared external services also need an operator lifecycle
separate from individual products and the platform repository.

## Decision

Recognize the existing independent Orin repository and preserve its name.
Keep Mind-Seed as the canonical core for Mind-Seed, OS as the platform owner,
and .github as public governance.

Authorize one next private repository, `mind-seed-infrastructure`, for shared
service configuration and recovery. Record it as a creation target until its
existence and initialization are verified. The initial website source stays
with Mind-Seed; future extraction follows substantive evidence.

The [repository layout](../../repository-layout.md) defines the boundaries and
creation/registration procedure. No per-subdomain repositories are created.

## Alternatives considered

- Keep operations inside a product: workable initially, but shared service
  credentials, recovery and delivery would have unclear cross-product ownership.
- Put every service in OS: conflates product/service delivery with platform policy.
- Split every future subsystem now: creates empty repositories and speculative
  compatibility commitments.
- Create separate mail and website repositories now: the initial service
  configuration can share an operations lifecycle; website source extraction
  is not yet substantiated.

## Consequences

One creation target is justified; all other candidates remain with current
owners. Orin's runtime and local source work are not modified or claimed
complete. Repository existence, initialized source, validation and deployment
remain separate facts. Private operations and credentials stay outside public
governance.

## Dependencies

Existing organization repository policy, current GitHub inventory and
maintainer authorization. Repository creation requires a supported authenticated
administration surface. No paid plan, external app, team or visibility change
is required by this decision.

## Supersession

This refines the repository snapshot and future-component discussion of
[ADR-0001](ADR-0001-organization-boundary.md). Its no-placeholder rule remains.
[ADR-0002](ADR-0002-os-platform-peer.md) retains platform ownership.
Neither earlier ADR is wholly superseded.

## Evidence and verification

On 2026-09-05 the authenticated repository listing showed `.github`,
`Mind-Seed`, `OS` and `Orin`; Orin's source initialization was not established.
The owner authorized minimal repository creation in the current task.
The organization manifest includes existing repositories only. Offline schema,
semantic, link and regression checks verify the documentation change; they
cannot prove service deployment or unpublished local source state.

## Creation completion — 2026-09-05

The authorized target was created privately and initialized on `main` at
`6c0b15235a370387606f3dac19ad6528d633205b`. Published source readback matched
the prepared foundation. The organization manifest now registers its
experimental source lifecycle and shared-service ownership; the original
creation-target wording above records the decision before execution.
See [shared-service governance](../../organization-architecture.md#shared-service-governance)
for verification scope. No operational activation or Orin source work is claimed.

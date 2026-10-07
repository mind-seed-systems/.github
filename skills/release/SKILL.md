---
name: release
description: Prepare and complete the repository's normal release workflow, including versioning, notes, tags, artifacts, or release records where applicable.
---

# Release

## Shared contracts

- [core](../../.agent/contracts/core.md)
- [authorization](../../.agent/contracts/authorization.md)
- [verification](../../.agent/contracts/verification.md)
- [git-github](../../.agent/contracts/git-github.md)
- [deployment](../../.agent/contracts/deployment.md)
- [handoff](../../.agent/contracts/handoff.md)

## Project context

Read [project metadata](../../.agent/project.yaml) and the relevant entries in
[workflows](../../.agent/workflows/README.md) and
[integrations](../../.agent/integrations/README.md). For public metadata changes,
use the shared public metadata workflow. Paths in prose are repository-relative.
Load memory and scopes only for persistent context, registry, cross-project
relationships or promotion; ordinary work does not require those contracts.

## Workflow and completion

1. Identify the intended version/source, release authority and actual release
   configuration: versioning, notes, tags, artifacts and release records.
2. Reconcile existing tags/releases to avoid duplicate or conflicting identities.
3. Prepare only the configured artifacts and notes; verify their provenance.
4. Execute the authorized release workflow after applicable checks and read back
   its actual tag, artifacts and published release record.

This repository has no defined product release mechanism. A generic request
therefore needs a concrete release target/process before mutations; report that
limit instead of inventing package versions or a hosted pipeline. Complete any
independent authorized preparation. Ordinary completed work belongs to `push`.
Release is distinct from deployment and does not prove live behavior.

Completion requires the configured release evidence. Handoff identifies source,
version, artifacts and any separate deployment state or outstanding blocker.

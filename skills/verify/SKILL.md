---
name: verify
description: Independently verify claimed repository, branch, PR, release, deployment, or live state using current evidence.
---

# Verify

## Shared contracts

- [core](../../.agent/contracts/core.md)
- [verification](../../.agent/contracts/verification.md)
- [handoff](../../.agent/contracts/handoff.md)

## Project context

Read [project metadata](../../.agent/project.yaml) and the relevant entries in
[workflows](../../.agent/workflows/README.md) and
[integrations](../../.agent/integrations/README.md). For public metadata changes,
use the shared public metadata workflow. Paths in prose are repository-relative.
Load memory and scopes only for persistent context, registry, cross-project
relationships or promotion; ordinary work does not require those contracts.

## Workflow and completion

1. Identify the exact claim, target revision/surface and acceptance conditions.
2. Retrieve current source evidence independently of prior handoffs or agent claims.
3. Run the strongest proportional check available and compare its observations
   with each claim; retain the target identity needed to interpret the result.
4. Classify results using the verification contract without weakening criteria.

Load Git/GitHub for branch/PR claims and deployment for release/live claims.
Do not repair the implementation unless the assigned task also authorizes that
work. `review` searches a change for defects; this workflow tests specific claims.
A static link check is not provider discovery or live acceptance.

Completion requires an explicit verdict per material claim, supporting evidence
and unverified limits. Keep local, remote and live evidence separate.

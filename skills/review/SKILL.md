---
name: review
description: Review a change, branch, pull request, or implementation for material correctness, regression, architecture, security, and maintainability issues.
---

# Review

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

1. Establish scope, base/head revisions, intended behavior and affected consumers.
2. Inspect the change and surrounding contracts; load Git/GitHub for branches/PRs.
3. Prioritize correctness, requested behavior, regressions, contracts, architecture,
   security, tests, maintainability, relevant performance/accessibility, then
   material style concerns.
4. Verify suspected issues with source or a focused safe check when possible.
5. Report actionable findings with severity, location, trigger, impact and remedy.

Do not bury defects under style noise or invent findings to fill a review.
Distinguish confirmed defects from questions and residual test risk. `verify`
checks named claims; `fix` applies authorized repairs. Reviewing does not by
itself authorize posting external comments or changing implementation.

Completion is a candid review, including no findings when appropriate, with
material gaps and the inspected revision. A self-review is not an externally
required independent approval.

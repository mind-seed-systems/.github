---
name: build
description: Implement substantial repository changes and carry them through relevant verification and normal repository completion workflow.
---

# Build

## Shared contracts

- [core](../../.agent/contracts/core.md)
- [authorization](../../.agent/contracts/authorization.md)
- [verification](../../.agent/contracts/verification.md)
- [git-github](../../.agent/contracts/git-github.md)
- [handoff](../../.agent/contracts/handoff.md)

## Project context

Read [project metadata](../../.agent/project.yaml) and the relevant entries in
[workflows](../../.agent/workflows/README.md) and
[integrations](../../.agent/integrations/README.md). For public metadata changes,
use the shared public metadata workflow. Paths in prose are repository-relative.
Load memory and scopes only for persistent context, registry, cross-project
relationships or promotion; ordinary work does not require those contracts.

## Workflow and completion

1. Establish task scope, relevant source, current Git baseline and acceptance.
2. Inspect existing implementation and consumers; choose the smallest coherent
   change preserving the repository's public-information boundary.
3. Implement the end state, update stale canonical documentation and run relevant
   native checks. Repair task-caused failures rather than weakening criteria.
4. Review the task diff and complete its authorized Git/GitHub endpoint.

Use this for substantial new behavior or repository infrastructure. A known defect
belongs to `fix`. `develop` is an alias for this workflow. New dependencies or
architecture need a task-related reason. Do not automatically release, deploy or
publish because implementation is complete.

Completion requires the requested behavior, relevant verification and the
applicable repository delivery endpoint. Report material decisions and remaining
blocked acceptance separately.

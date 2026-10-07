---
name: push
description: Finalize completed local work through the repository's normal commit, push, pull-request, check, and merge workflow.
---

# Push

## Shared contracts

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

1. Inspect local status, branch/upstream, completed changes and live matching PRs.
2. Verify the task diff and relevant checks; preserve unrelated work and stage
   only reviewed task paths into coherent commits.
3. Push, create or update the PR and inspect current head checks/reviews.
4. Remediate task-caused failures, merge when authorized and requirements pass,
   and verify the resulting remote/default branch.

Use this to deliver completed local work. If substantial implementation remains,
use `build` or `fix` for that part rather than claiming the changes are ready.
`release` owns versions/tags/artifacts; this workflow does not create them by
implication. Inspect indirect publication effects before remote mutations.
A narrower endpoint in the user's task constrains the standing workflow.

Completion is the actual authorized repository endpoint. Report commit, PR,
checks, merge identity and any non-required failures without calling them passed.

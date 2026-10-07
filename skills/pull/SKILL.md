---
name: pull
description: Safely synchronize local repository state with upstream while preserving unrelated work and reconciling conflicts according to repository conventions.
---

# Pull

## Shared contracts

- [core](../../.agent/contracts/core.md)
- [authorization](../../.agent/contracts/authorization.md)
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

1. Inspect local status, worktrees, branch, remote and upstream before fetching.
2. Fetch and compare divergence; identify task-owned and unrelated local changes.
3. Fast-forward when possible. For divergence follow the Git/GitHub contract's
   safe merge/rebase rules and resolve only conflicts whose intent is established.
4. Check the resulting local revision, preserved changes and affected behavior.

Do not use reset, clean or stash as a default synchronization strategy. If safe
integration would touch concurrent work, leave it intact and isolate or report
the specific conflict. Merely asking how far behind a branch is belongs to
`investigate`; this workflow actually synchronizes state.

Completion requires verified local/upstream relationship and preserved work.
Report remaining divergence or conflicts accurately. It does not imply pushing,
merging a PR or retiring any unreviewed local branch.

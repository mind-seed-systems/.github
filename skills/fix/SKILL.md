---
name: fix
description: Diagnose and repair a known defect, failed check, incomplete prior change, review finding, or inconsistency between authoritative project states.
---

# Fix

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

1. Reproduce or substantiate the reported defect, failed check or inconsistency.
2. Trace the cause and determine which state is authoritative for each data type.
3. Repair the cause with a bounded change preserving unrelated work and behavior.
4. Add or run meaningful regression checks where the defect warrants them;
   rerun affected checks and reconcile documentation.
5. Complete the authorized Git/GitHub workflow and verify its actual endpoint.

`reconcile` invokes this skill with state-reconciliation intent. Distinguish source,
documentation, Git, GitHub, runtime/deployment, registry, memory and prior handoffs.
Do not duplicate work objects or force states to agree by deleting evidence.
Load memory/scope contracts only when reconciliation crosses persistent context.
Use `build` for new behavior, not to disguise a causal repair as a redesign.

Completion requires evidence that the defect is repaired and adjacent behavior
preserved. Report the cause, validation and actual delivery state.

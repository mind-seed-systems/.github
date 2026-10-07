---
name: investigate
description: Inspect repository, runtime, or work state to establish current behaviour, root cause, or required work without changing implementation by default.
---

# Investigate

## Shared contracts

- [core](../../.agent/contracts/core.md)
- [handoff](../../.agent/contracts/handoff.md)

## Project context

Read [project metadata](../../.agent/project.yaml) and the relevant entries in
[workflows](../../.agent/workflows/README.md) and
[integrations](../../.agent/integrations/README.md). For public metadata changes,
use the shared public metadata workflow. Paths in prose are repository-relative.
Load memory and scopes only for persistent context, registry, cross-project
relationships or promotion; ordinary work does not require those contracts.

## Workflow and completion

1. Turn the question into observable hypotheses; inspect relevant local source,
   configuration, logs or current remote work state without changing implementation.
2. Trace the causal path and check competing explanations against direct evidence.
3. Separate observations, supported conclusions, inference and unknowns.
4. Describe the root cause or remaining uncertainty and bounded next work.

Use `research` when the missing evidence is primarily external technical material.
Use `fix` only when repair is requested; discovering a defect does not authorize
implementation. Load the Git/GitHub contract when interpreting branch/work state.
Read-only remote inspection is allowed within access and disclosure boundaries.

Completion is an evidence-backed answer, not a code change. Handoff should name
the relevant files or observations, confidence limits and the smallest remaining
experiment if the cause is unresolved.

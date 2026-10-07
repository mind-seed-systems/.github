---
name: research
description: Research external technical evidence, standards, APIs, libraries, or alternatives needed for a repository decision or implementation.
---

# Research

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

1. Frame the repository decision, constraints and unknown external facts.
2. Use current primary sources for technical specifications, supported APIs,
   provider behavior and standards. Track version, publication context and links.
3. Compare applicable alternatives against actual repository needs and costs.
4. Separate repository evidence, external evidence, inference and recommendation.

Default to research-only. Do not implement recommendations or create a new
persistent document unless that deliverable is requested or repository policy
requires it. `investigate` handles repository/runtime root cause; researching an
API is not a reason to scan unrelated private projects.

Completion requires a sourced answer that resolves the decision or identifies
missing evidence. Report material tradeoffs and uncertainties without presenting
recommendations as already accepted architecture.

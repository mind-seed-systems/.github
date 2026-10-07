---
name: publish
description: Force-publish the intended state by bypassing only eligible repository or deployment-process gates while preserving external platform protections.
---

# Publish

## Shared contracts

- [core](../../.agent/contracts/core.md)
- [authorization](../../.agent/contracts/authorization.md)
- [verification](../../.agent/contracts/verification.md)
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

1. Establish an explicit force-publication request, intended state and target.
2. Identify why normal deployment is blocked and who controls each gate.
3. Confirm authority for the effect and for any eligible local/process bypass.
4. Apply only the minimum eligible bypass defined by the deployment contract.
5. Preserve failed/skipped results truthfully and verify the resulting live state.

A generic request to publish content normally may mean `deploy`; do not infer
force semantics from the word alone when no gate bypass was requested.
Branch rulesets, required checks/reviews, environment approvals, organization
policy, hosting protections and IAM are never eligible bypass targets. Admin
capability is not permission. Stop the blocked action if the gate is external;
complete independent preparation and state the required authorized resolution.

Completion requires actual live evidence and an accurate list of intentionally
bypassed eligible gates. A forced push is not a substitute for this workflow.

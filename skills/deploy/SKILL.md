---
name: deploy
description: Deploy the intended repository state through its normal governed deployment process and verify the resulting live state.
---

# Deploy

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

1. Identify intended source, target environment, effect-specific authority and
   the actual normal deployment configuration.
2. Inspect required checks, external controls, migration prerequisites and health
   acceptance; resolve missing evidence before changing the target.
3. Execute the normal authorized process and observe its resulting identity.
4. Verify the relevant live surface and report failures or rollback needs.

Load Git/GitHub when delivery uses branches/PRs. This repository's normal public
metadata path is documented in the deployment contract; no application host is
configured. Do not invent a deployment service or modify another repository.
Never reinterpret a blocked deployment as `publish`; external approvals remain
binding even with administrator credentials.

Completion requires observed target state, not merely a passing build or merged
commit. Handoff distinguishes deployed identity, health and unavailable live proof.

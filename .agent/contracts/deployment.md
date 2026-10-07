# Release, deployment and publication

Release manages versions, tags, artifacts and release records; it does not
inherently make software live. Discover actual release mechanics before acting.
This metadata repository defines no versioned product release or application
hosting pipeline. Do not invent one or imply another project's release state.

Deploy follows the normal governed path, required checks, provider policy,
external controls, migration requirements and health criteria. Never silently
switch a blocked deploy into forced publication. Establish effect, target,
authority and acceptance before executing a live change.

Here, merging public metadata makes Git content public and GitHub may consume
profile/community files as organization defaults. Check the relevant public
GitHub surface when live acceptance of those files is part of the task. A push
of toolkit files is not proof that an agent has loaded them. Repository Git
workflow authorization covers publication of approved non-sensitive repository
content; it does not authorize private disclosure or hosted application changes.

## Publish semantics

Publish is an explicitly requested force-publication workflow. Identify the
normal blocker, classify who controls it, establish effect-specific authority,
and use the minimum eligible bypass. Only repository-controlled or
deployment-process-controlled gates may be eligible; local ownership alone does
not make a gate eligible. Organization governance remains binding.

Never bypass or administratively circumvent branch protections, rulesets,
externally required checks/reviews, protected environment approvals, organization
rules, hosting protections, IAM, cloud policy or equivalent external controls.
Credentials and administrator capability do not change that boundary.

Report failed/skipped checks truthfully, including each intentionally bypassed
local gate and the authority covering it. Verify the actual resulting live state.
If the blocker is external, stop that action and identify the required authorized
resolution. Complete independent preparation without weakening the control.

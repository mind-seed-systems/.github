# Governance and ownership

Mind Seed Systems is currently maintained by one verified organization owner,
[`@jikovec`](https://github.com/jikovec). Governance is intentionally light:
the goal is clear authority and recoverability for one or two trusted
maintainers, not a simulated enterprise hierarchy.

## Current ownership model

- The organization owner is the administrative recovery authority.
- Every repository names an accountable maintainer in the organization
  manifest and, where supported, `CODEOWNERS`.
- The canonical core repository owns cross-cutting Mind Seed product and system
  architecture until an extraction decision assigns a coherent artifact to a
  different repository.
- Material architecture decisions are recorded as repository-native ADRs.
- Security-sensitive incidents and credentials are handled outside public
  issues and source control.

No standing `core`, `security`, `infrastructure`, or `interface` teams are
created while each would contain the same single person. When a second
maintainer has a durable responsibility, create the smallest useful team and
move the matching ownership entries from an individual to that team.

## Change paths

Trusted maintainers may use direct, coherent commits to `main` when repository
protections, risk, and current automation permit it. Pull requests are preferred
for architectural, security-sensitive, migration, release, or independently
reviewed work, but are not bureaucracy imposed on every one-person change.

Direct changes and pull requests follow the same evidence rules: inspect first,
preserve unrelated work, run proportionate checks, document architectural
effects, and distinguish local implementation from live or release evidence.

## Administrative recovery

Where GitHub plan features permit branch or ruleset protection, `main` must
block deletion and force pushes while retaining an organization-owner recovery
path. Recovery bypass is for restoring access or repairing policy failures, not
ordinary development. Any use should leave a dated, non-sensitive record of
the reason, exact action, and resulting state.

Repository deletion, transfer, archival, visibility changes, member changes,
billing, external app installation, secret rotation, and published-history
rewrites always require a separate explicit decision.

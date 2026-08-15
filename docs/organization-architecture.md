# Mind Seed Systems GitHub architecture

**Status:** accepted organization baseline

**Last reviewed:** 2026-08-15

## Organization purpose

`mind-seed-systems` is the canonical GitHub boundary for Mind Seed and its
future independently owned components. Mind Seed is a local-first,
OS-integrated personal AI research system. The organization is intended to make
ownership, dependencies, evidence, security, and change history legible to both
maintainers and future AI agents.

The organization is the project boundary; the `Mind-Seed` repository is the
current canonical core. Those statements do not mean that every future artifact
belongs in the core, or that every named subsystem deserves a repository.

Capability language uses four states:

- **Implemented**: source or configuration exists at an identified revision.
- **Experimental**: implementation exists but its supported or operational
  boundary is not established.
- **Planned**: a reviewed direction or extraction trigger exists without the
  claimed implementation.
- **Conceptual**: a possibility is recorded for research or navigation only.

Repository presence, a passing local test, a tag, an Actions run, and a live
deployment are separate evidence classes.

## Repository tiers

### A. Existing canonical repository

#### `mind-seed-systems/Mind-Seed`

`Mind-Seed` is the private canonical core and the historical Ardor lineage. It
owns cross-cutting system behavior while that behavior changes together:

- executive runtime, cognition, goals, commitments, and bounded background
  operation;
- working, episodic, semantic, procedural, project, and governed long-term
  memory contracts;
- agent and tool orchestration, authority, approvals, evidence, recovery, and
  audit behavior;
- first-class NixOS package, service, sandbox, broker, and host-capability
  integration until a proven independent lifecycle exists;
- core APIs and protocols until multiple independently versioned consumers
  make a stable compatibility boundary necessary;
- shared specifications, schemas, tests, architecture, research, and release
  evidence for the core system;
- historical Ardor source and artifacts until a deliberate preservation or
  migration decision says otherwise.

The core does not automatically own a future independently deployed service,
standalone SDK, public website, distributable interface, or integration whose
release and security boundary can be managed independently. It also does not
absorb unrelated projects merely because they are accessible on the same
machine.

No monorepo split is part of this organization bootstrap. Extraction requires
substantive material, a stable interface, migration and rollback plans, and
evidence that the new boundary reduces ownership ambiguity rather than merely
moving files.

### B. Organization infrastructure

#### `mind-seed-systems/.github`

The public `.github` repository owns non-sensitive GitHub organization
metadata: the profile, shared contribution and security guidance, default issue
forms, pull-request guidance, optional workflow templates, label definitions,
the repository standard, ADR convention, and the machine-readable organization
manifest.

It is public only because GitHub requires the special repository to be public
for organization-wide defaults and the organization profile. Private source,
local operational evidence, adjacent-project details, credentials, and
unpublished internal plans do not belong here.

### C. Future component repositories

The following are architectural domains, not repository reservations:

| Domain | Default owner now | A separate repository becomes justified when |
| --- | --- | --- |
| Core/runtime | `Mind-Seed` | a runtime artifact can be released and supported independently of the executive core |
| Cognition | `Mind-Seed` | a coherent engine exposes a stable interface and has its own compatibility lifecycle |
| Memory | `Mind-Seed` | a substantive storage/service implementation owns durable schemas, migration, retention, and deployment independently |
| Agent orchestration | `Mind-Seed` | the orchestrator becomes a reusable artifact for multiple independently versioned consumers |
| Integrations | `Mind-Seed` adapters | one integration has substantial code, independent credentials/security review, and a separate release cadence |
| Protocols / SDK / API | `Mind-Seed` | multiple repositories consume a stable versioned protocol or SDK |
| System integration | `Mind-Seed` | packaging or host integration becomes independently consumable without separating Mind Seed from its NixOS target |
| UI / interfaces | `Mind-Seed` | a desktop, web, mobile, or embodied interface has a separately distributable artifact and compatibility contract |
| Infrastructure | `.github` for GitHub metadata; core otherwise | deployment or build infrastructure owns independent environments and lifecycle |
| Research / evaluation | `Mind-Seed` | a substantial reusable, rights-cleared benchmark or knowledge corpus has independent governance |
| Website / distribution | none | an approved public beta creates a real website, download, or deployment boundary |
| Security | cross-cutting | a substantive independently maintained security tool or policy artifact exists; security responsibility itself remains cross-cutting |

Likely future names use `mind-seed-<component>`, for example
`mind-seed-memory` or `mind-seed-sdk`, only after the corresponding decision is
accepted. A component with an established standalone product identity may keep
that identity when the exception and relationships are documented.

## Current repository map

| Repository | Visibility | Role | Lifecycle | Release state | Default branch | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| `.github` | Public | Organization metadata and standards | Active | Not applicable | `main` | `@jikovec` |
| `Mind-Seed` | Private | Canonical core and Ardor lineage | Experimental | Internal / unreleased | `main` | `@jikovec` |

GitHub's API is authoritative for current existence, visibility, default branch,
and repository state. The
[organization manifest](../mind-seed-organization.json) is authoritative for
semantic roles and relationships. A stale manifest must be corrected; it must
not override live GitHub state.

## Repository creation policy

A new repository requires all of the following:

1. a coherent artifact, runtime, service, interface, infrastructure layer, or
   knowledge domain;
2. an accountable owner and purpose;
3. substantive existing material, not a placeholder README;
4. an independent lifecycle, deployment boundary, or clear ownership problem
   that the core cannot represent cleanly;
5. explicit dependencies and relationship edges;
6. security classification, data ownership, credentials boundary, and threat
   considerations;
7. documentation, version/release policy where applicable, and proportionate
   CI;
8. a migration and rollback plan when extracting existing material;
9. an update to the organization manifest and repository map.

A name appearing in a roadmap, concept note, architecture diagram, or issue is
not sufficient. If the boundary is uncertain, record an ADR and keep the work
in the current owner until evidence resolves it.

## Ownership model

The current organization has one primary owner. Ownership is recorded using
the actual maintainer identity, `@jikovec`; no fictional departments or teams
exist. A future team is created only when at least two people need a durable
shared responsibility or GitHub access boundary.

Suggested future teams are `core-maintainers`, `security`, `infrastructure`,
and `interfaces`. Creating them is a later access-governance decision, not part
of the current bootstrap.

## Branch and Git strategy

- Default branch: `main`.
- Development model: trunk-based, with short-lived branches when review,
  isolation, or CI warrants them.
- Shared published history is not rewritten for aesthetics.
- Primary branches block deletion and force pushes where the repository plan
  supports protections; the organization owner retains an administrative
  recovery path.
- Pull requests are expected for material architecture, security, migrations,
  releases, or independent review. They are not mandatory bureaucracy for every
  low-risk maintainer change.
- Commits use a lightweight Conventional Commits shape when useful and remain
  coherent, readable, and scoped.

See [the repository standard](repository-standard.md) for the complete baseline.

## Issues and labels

Default forms cover bugs, capability proposals, architecture/RFC proposals,
and research tasks. Security-sensitive reports never use public issues.

Labels have five orthogonal dimensions:

- `type:*` — what kind of work it is;
- `priority:P0` through `priority:P3` — urgency and impact;
- `state:*` — workflow state that GitHub does not already express;
- `area:*` — owning architectural domain;
- characteristics such as `breaking-change`, `dependencies`, `performance`,
  and `privacy`.

Repositories receive only applicable area/type labels. Unknown custom labels
are preserved by the synchronization helper; it removes only known unused
GitHub defaults when explicitly requested.

## Pull requests

The shared template asks for purpose, architectural scope, implementation,
important decisions, tests and evidence, security/privacy effects, memory/data
migration, compatibility, documentation, rollout, and unresolved risk. Fields
may be marked not applicable; contributors should not manufacture content to
fill a template.

## Architecture decisions

Material decisions live under `docs/architecture/decisions/` in the repository
that owns the decision. Each record has a stable ID, title, status, date,
context, decision, alternatives, consequences, dependencies, and explicit
`supersedes` / `superseded-by` relationships. Stable metadata and links allow
future agents to traverse decision history without treating an old record as
current policy.

## Cross-repository relationship model

Organization membership is an access and hosting fact, not a complete semantic
graph. The organization manifest supports these directed relationship types:

| Relationship | Meaning |
| --- | --- |
| `contains` | source owns a logical component or bounded artifact represented by target |
| `depends-on` | source requires target at build, runtime, operation, or governance time |
| `integrates-with` | peers communicate through a documented boundary without ownership |
| `implements` | source realizes a target protocol, specification, or design |
| `extends` | source adds optional behavior while preserving the target boundary |
| `provides-interface-for` | source owns an interface consumed by target |
| `research-supports` | source supplies provenance-aware evidence for a target decision |
| `deployed-by` | source's artifact is deployed by target infrastructure |
| `supersedes` | source replaces target under a recorded migration decision |
| `related-to` | a meaningful non-authoritative association not captured above |

Every edge has a lifecycle status and evidence reference. A relationship never
grants repository, filesystem, credential, data, network, or deployment
authority. This graph complements future filesystem and project-memory graphs;
it does not replace their finer-grained provenance or access controls.

Adjacent projects, personal machine configuration, external products, and
other companies remain external unless a separate transfer or ownership
decision changes that fact. Conceptual integration does not move their code or
data into this organization.

## Machine-readable organization knowledge

[`mind-seed-organization.json`](../mind-seed-organization.json) records only
semantic facts that GitHub does not reliably derive: repository roles,
component ownership, lifecycle classification, release posture, documentation
authorities, and typed relationships. Live inventory, branches, permissions,
issues, checks, and releases remain dynamic GitHub data.

The manifest is intentionally small, schema-backed, and validated by
`scripts/validate_organization.py`. Extensions require a schema version or an
explicit optional field rather than ad-hoc undocumented keys.

## Security baseline

- Repositories are private by default; a public repository requires an explicit
  non-sensitive purpose.
- `GITHUB_TOKEN` defaults to read-only; write permissions are granted only per
  job and purpose.
- Third-party Actions are pinned to immutable commit SHAs.
- Dependency graph and Dependabot alerts/security updates are enabled where
  the plan supports them and a repository has relevant manifests.
- Secret scanning, push protection, code security, private vulnerability
  reporting, branch protection, and rulesets are enabled only where supported
  without a paid change and without changing private source visibility.
- No required status check is configured until the exact check has run reliably
  on the repository.
- No secret, member, billing, visibility, external-app, or credential change is
  inferred from this baseline.

The current GitHub Free organization cannot enforce branch protection or
rulesets on private repositories. This is a plan limitation, not a reason to
make the core public. The policy remains documented and should be enabled if a
future approved plan or visibility decision makes it available.

## CI and automation strategy

CI belongs with the artifact it verifies. Organization templates provide a
least-privilege starting point, not a mandatory language stack. Repositories
should begin with deterministic, CPU-bounded checks that already work locally.
GPU, model, live provider, protected-vault, deployment, and long-duration jobs
require explicit environment, cost, credential, and authorization decisions.

Reusable or shared workflows are introduced only after two repositories need
the same stable behavior. Release automation must fail closed and must not gain
write permissions merely because a local build passes.

## Release model

Independently released software uses Semantic Versioning. A repository may use
these lifecycle stages without claiming it has reached them:

| Stage | Meaning |
| --- | --- |
| Experimental / internal | research and development; no supported public contract |
| Alpha | intentionally limited public testing with breaking change expected |
| Beta | documented supported surface under broader testing; remaining gates explicit |
| Stable | versioned compatibility and support policy backed by operational evidence |

A release identifies the exact version and scope, implemented capabilities,
verification level, known limitations, compatibility and migration effects,
and unresolved operational gates. Meaningful releases update the repository
changelog and GitHub Releases. A local implementation, tag, workflow definition,
or green test run does not alone prove deployment or release acceptance.

Existing Mind Seed release/version history is preserved. No version is created
by this organization bootstrap.

## GitHub Project structure

When organization Projects access is available to the authenticated owner, the
canonical project is **Mind Seed Development** with these fields:

- Status
- Priority
- Area
- Repository
- Target Release
- Risk
- Type

Its views are Current work, Roadmap, Backlog, Architecture, Research, and
Security / technical debt. Only actual issues and pull requests are added;
placeholder roadmap items are not invented. Project configuration is dynamic
GitHub state and is not duplicated into the organization manifest.

## AI-agent operation

Agents follow [the AI-agent contribution policy](ai-agent-contributions.md):
inspect before editing, preserve scope and user work, cite architecture evidence,
use least authority, run checks, report exact evidence, and keep implementation,
deployment, and acceptance distinct. An agent's tool access is capability, not
authorization.

## Current limitations

- The private core remains experimental and has no accepted public release.
- Organization-wide defaults are public and therefore intentionally omit
  private architecture evidence and adjacent-project details.
- Private-repository branch protection/rulesets and advanced secret/code
  scanning are unavailable on the current GitHub Free organization plan.
- A public vulnerability contact beyond supported GitHub private-reporting
  surfaces has not been designated.
- A second-maintainer team model is documented but not yet needed.
- Future extraction candidates remain in the core until their criteria are met.

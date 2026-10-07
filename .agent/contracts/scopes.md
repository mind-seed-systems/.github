# Scope semantics

Scopes describe identity, lifetime and visibility; nesting is not a universal
override hierarchy. Authority follows data type and governing provenance.
Visibility below is always bounded by configured permissions and disclosure rules.

| Scope | Identity and lifetime | Read visibility | Write authority | Inheritance and promotion | Status |
| --- | --- | --- | --- | --- | --- |
| global | Established cross-project identity; durable | Only permitted global context | Authorized global owner/grant | Shared context may flow down; promotion from organization requires global write authority | Context unless designated policy for its domain |
| organization | Verified organization ID; organization lifetime | Permitted organization context | Governing organization authority | Lower scopes may narrow, never widen prohibitions; promotion from project needs organization authority | Organization identity/policy authoritative in its domain |
| project | Canonical project binding, possibly many repositories; project lifetime | Permitted project context | Project owner or valid delegation | Inherit applicable organization rules; promote task findings only after canonical adoption and project write grant | Project identity/accepted decisions authoritative; memory contextual |
| repository | Canonical host/owner/name; repository lifetime | Current permitted source/work state | Applicable repository/task grant | Refines execution rules; cannot rewrite project identity; durable decisions use accepted repository workflow | Technical source and accepted repository policy authoritative in domain |
| agent | Verified executor identity; agent lifetime | Only delegated/available scopes | Only delegated rights | Carries context, never self-grants; upward writes use destination authority | Executor context, not higher identity/policy |
| task | Assigned work identity; task lifetime | Task-relevant permitted context | Task scope plus valid grant | May narrow work; promotion to project requires source reconciliation and destination authority | Intent can authorize allowed task effects; findings contextual |
| session | Runtime interaction identity; session lifetime | Session-visible permitted context | Session-bound task authority | Findings remain ephemeral; promotion to task requires task authority and supported persistence | Observations/context, not durable policy |

A session cannot change project identity; a task cannot redefine an organization;
an agent cannot mint canonical registry IDs for convenience. Technical repository
truth is not overridden by project, agent, task or session memory. Task intent
may grant actions allowed by authorization policy; memory/session state cannot.
Repository instructions refine generic behavior, while task/session narrowing
cannot silently remove governance or safety boundaries.

Promotion (`session -> task`, `task -> project`, `project -> organization`,
`organization -> global`) is an explicit write, never automatic. Each destination
must permit the write, the information must fit its scope, authority must cover
mutation, canonical source/registry decisions must be updated first where
applicable, and the persistence mechanism must support it. Read access or lower
scope ownership is not promotion authority. Use [memory](memory.md) for persistence.

Bindings in `.mind-seed/scopes.yaml` instantiate these semantics. Null external
IDs are unresolved and unusable, not wildcard scopes. Repository-qualified
public identities are distinct from registry-owned scope IDs.

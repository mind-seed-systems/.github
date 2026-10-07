# Persistent memory contract

> Memory is contextual state, not repository truth.

Memory never overrides current source, configuration, tests, schemas, manifests,
Git, GitHub operational state, live evidence or accepted repository decisions.
It can guide discovery, supply historical context, point to accepted decisions,
retain user-approved durable context and link relationships within read scope.
Reconcile it before treating it as current fact; stale context is not authority.

Determine configured backend, scope visibility, permissions and freshness before
reading. Use [scope semantics](scopes.md) and verified bindings. When source
conflicts with memory, source wins for its data type. Do not silently repair
persistent memory simply because it is stale.

Writes need a writable destination, explicit or standing mutation authority,
appropriate content and supported persistence. Access alone is insufficient.
Apply authorized promotion rules; never automatically persist session observations,
task hypotheses, temporary failures or unverified interpretations. Do not write
memory merely to log ordinary work. Never persist secrets, tokens, private keys
or unnecessary sensitive runtime content.

Record durable technical decisions in the repository's accepted decision surface
first, then commit/adopt them before or with an authorized memory pointer/summary.
Preserve ADR/Issue/PR references instead of copying canonical content. No live
mutable memory belongs in Git by default. In this public repository,
GOVERNANCE.md also limits which durable facts may be recorded at all.

`.mind-seed/memory.yaml` is a binding, not a store. Until a backend and scopes
are verified and authority granted, its empty permissions permit no integration
reads or writes. Session tools or global memory do not silently populate it.

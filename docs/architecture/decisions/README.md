# Architecture decision records

Material organization decisions use immutable IDs and explicit lifecycle
metadata so maintainers and agents can traverse current and superseded policy.

Filename format: `ADR-NNNN-kebab-case-title.md`.

Start a record with:

```yaml
---
id: ADR-0000
title: Concise decision title
status: proposed
date: YYYY-MM-DD
decision_owners:
  - "@owner"
supersedes: []
superseded_by: null
---
```

Allowed statuses are `proposed`, `accepted`, `deprecated`, `superseded`, and
`rejected`. An accepted record is not edited to disguise a later change;
create a new ADR, set the relationship fields in both records, and preserve the
historical context.

Each record contains these sections:

1. Context
2. Decision
3. Alternatives considered
4. Consequences
5. Dependencies
6. Supersession
7. Evidence and verification

Repository-specific ADRs live in the repository that owns the decision. This
directory owns organization-wide decisions only.

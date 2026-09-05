# Minimal repository structure

Status: owner-authorized direction; existence and initialization tracked separately.

| Repository | Responsibility | Current disposition |
| --- | --- | --- |
| `.github` | Public organization governance, standards and semantic inventory | Existing |
| `Mind-Seed` | Core product, application contracts, integrations and initial website source | Existing |
| `OS` | Platform composition, host policy, storage and system recovery | Existing |
| `Orin` | Independent research project, its source and identity semantics | Existing; separate initialization work |
| `mind-seed-infrastructure` | Shared external-service operations, domain/DNS configuration, service deployment and service recovery | Authorized next creation; not yet in live inventory |

## Why one new repository

Shared services must be maintainable without releasing either product, and
their operator credentials and recovery procedures need a distinct boundary.
The infrastructure repository owns service delivery and operational evidence;
consuming products own adapters, permissions and application behavior.
The OS repository continues to own platform and physical-host policy. A service
repository does not silently gain authority over a host.

Website source remains with Mind-Seed. Infrastructure may deploy a reviewed
website artifact by immutable revision; it does not duplicate application source.
Public delivery of a website does not require public source visibility.

## Creation and registration

Create only `mind-seed-infrastructure`, private with default branch `main`,
owner `@jikovec`, infrastructure role, internal/unreleased posture. Initial
material must include the bounded service registry and validation, operational
state provenance, recovery and secret boundaries, and an ADR. Substantive
documentation/configuration does not imply deployable manifests or live service
acceptance.

After creating and initializing it:
1. Verify its identity, private visibility, default branch and initial commit.
2. Add `shared-services` to the organization repository manifest with that
   repository name and `experimental` lifecycle.
3. Add `external-service-operations` as a `current-repository` component domain.
4. Add governance provision as an active relationship. Record product/service
   integration as planned only when its contract is documented.
5. Update this map and run offline validation plus a complete live inventory
   comparison.

Never register a creation target as a live repository to make the manifest
appear complete. Record the exact creation result, including access failures.

## Later extraction criteria

Do not create repositories merely for subdomains, protocols or upstream tools.
Mail, DNS, certificates and tunnel configuration start as directories in the
shared-service repository. Do not create a downstream Stalwart fork for configuration.

Separate website, API, SDK, memory, synchronization, cache, authentication or
connector repositories require substantive owned material and an independent
release, compatibility, deployment or contributor-access boundary. Document
dependencies, migration and rollback before extraction. The existing repository
creation policy continues to apply.

## Transition

Preserve existing source and historical reports in place. Link new ownership
from the relevant indexes once the destination exists; migrate only specifically
reviewed material, preserving history and provenance. Orin's ongoing
initialization is independent and must not be overwritten with a README seed.

If the new infrastructure boundary proves premature, retain its work privately
and propose a reviewed consolidation. Do not automatically delete, archive,
transfer or rewrite any repository.

See [ADR-0003](architecture/decisions/ADR-0003-minimal-repository-growth.md).

# Integrations

GitHub is the configured external service for `mind-seed-systems/.github`.
Canonical local configuration is `.github/`, `config/labels.json` and
`workflow-templates/`; current remote settings, checks, Issues, PRs and Projects
must be retrieved from GitHub. Templates are distributable artifacts, not proof
of an active workflow. Use Git and authenticated `gh` or equivalent APIs.
Credentials come from the user's existing credential manager/CLI or CI-provided
scoped token; never commit them or print authentication material.

Read-only inspections are separate from mutation. Writes follow the authorization
and Git/GitHub contracts, including actual executor and authority in authored
GitHub text. Integration availability never creates permission.

Mind-Seed public bindings live under `.mind-seed/`. There is no configured
repository registry endpoint or memory backend. Their unresolved fields must not
be interpreted as a verified absent external registry. Do not fabricate IDs or
inspect private stores merely because they are reachable.

For a new real integration document its canonical configuration, external service,
read/write effects, environment/tools, project/organization binding and credential
source. Include only services actually configured or materially needed.

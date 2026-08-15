# Contributing to Mind Seed Systems

Mind Seed is currently a private research project maintained by a very small
trusted group. Contributions should optimize for coherent evidence and
maintainable architecture rather than process volume.

## Before changing anything

1. Read the target repository's `README`, local agent instructions, current
   state, architecture decisions, and verification commands.
2. Inspect the current source, configuration, Git state, and relevant history.
3. Confirm that the repository owns the artifact being changed. Use an
   architecture proposal when ownership or extraction is uncertain.
4. Keep credentials, personal data, protected knowledge, private machine
   details, model artifacts, and unapproved third-party material out of Git.

Use the default issue forms for bugs, capability proposals, architecture
decisions, and research tasks. Do not open a public issue for a suspected
vulnerability; follow [SECURITY.md](SECURITY.md).

## Development model

- Default branch: `main`.
- Model: trunk-based development for one or two trusted maintainers.
- Branches: short-lived when review or isolation is useful.
- History: never rewrite published shared history merely for aesthetics.
- Commits: use a lightweight Conventional Commits form when practical:
  `type(optional-scope): imperative summary`.

Common types are `feat`, `fix`, `docs`, `refactor`, `test`, `research`, `build`,
`ci`, `security`, and `chore`. One commit should tell one reviewable story; do
not mix unrelated user work or generated artifacts into it.

## Verification and evidence

Run the smallest checks that can falsify the change, followed by broader checks
when warranted. A change report must state:

- files changed;
- checks actually run and their results;
- checks skipped or unavailable and why;
- security, privacy, memory, compatibility, and migration effects;
- remaining gates and risks.

Use evidence terms literally. Source-present or locally tested work is not
live-verified, deployed, or released unless the exact external boundary was
observed and recorded.

## Architecture, data, and releases

Material architecture changes require an ADR or RFC. Data and memory changes
must define ownership, provenance, retention, migration, rollback, deletion,
and authorization effects. Independently released software uses Semantic
Versioning; meaningful releases update a changelog and GitHub Release notes for
the exact artifact identity.

Follow the [AI-agent rules](docs/ai-agent-contributions.md) for agent-authored
work. Generated-by-AI attribution is not required in every commit; the evidence
and review obligations are the same regardless of authoring tool.

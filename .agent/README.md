# Repository agent toolkit

Start at [AGENTS.md](../AGENTS.md) and [project.yaml](project.yaml). This portable
layer is usable without the optional [Mind-Seed bindings](../.mind-seed/project.yaml).
Canonical workflow bodies live in [skills/](../skills/); contracts own shared
policy, workflows own reusable local processes, and provider files only discover them.

Use `build` for implementation, `fix` for a known defect, `investigate` for local
questions, `research` for external evidence, `verify` for claims, `review` for
change risks, `push` for completed-work delivery and `pull` for synchronization.
`release`, `deploy`, and `publish` follow the separate deployment contract.
Aliases `develop` and `reconcile` select existing workflows rather than copies.

## Provider discovery

- Codex: `.agents/skills/` contains native adapters. `.codex/skills` is a relative
  compatibility symlink to that directory, satisfying older discovery surfaces
  without a second implementation. Use `$build` or request the workflow by name.
- Claude Code: `.claude/skills/` contains thin adapters; `CLAUDE.md` imports
  `AGENTS.md`. Use `/build` or request the workflow by name. The `release`,
  `deploy` and `publish` adapters also set `disable-model-invocation: true`, so
  Claude Code loads them only on an explicit `/release`, `/deploy` or `/publish`.
  Canonical skills and Codex adapters keep portable name/description metadata,
  and validation enforces both forms.
- Other agents: read `AGENTS.md`, then `skills/<name>/SKILL.md` directly.

All paths in adapter prose are relative to the repository root. Native discovery
is provider/version dependent; inspect the selected skill's path when global or
bundled skills share its name. Restart or refresh discovery after changes.
Keep metadata aligned with canonical frontmatter; validation detects drift.

Discovery references: [Codex skills](https://learn.chatgpt.com/docs/build-skills),
[Claude skills](https://code.claude.com/docs/en/skills), and
[Claude imports](https://code.claude.com/docs/en/memory).

## Extension points

- [Contracts](contracts/core.md): load the concern needed by the selected skill.
- [Workflows](workflows/README.md): public metadata editing shared by several skills.
- [Integrations](integrations/README.md): GitHub configuration and authority sources.
- [Hooks](hooks/README.md): deterministic toolkit validation in CI or manually.
- [Routing evaluations](evals/skill-routing.md): positive and negative cases.

Add `skills/project/<unique-name>/SKILL.md` and adapters only for a real recurring
repository-specific reasoning workflow. No such additional workflow or legacy
monolithic agent prompt exists in the baseline. Do not create speculative services,
release pipelines, registry entries or memory stores.

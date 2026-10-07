# Public metadata changes

Read GOVERNANCE.md and CONTRIBUTING.md before editing public content. Verify each
claim against current public repository evidence; do not turn private knowledge
into an inventory or claim about an internal system.

Inspect consumers of changed files:

- `profile/README.md`: public organization profile.
- Community files and `.github/ISSUE_TEMPLATE/`: GitHub organization defaults
  used where eligible repositories have no local overrides.
- `.github/pull_request_template.md`: default PR evidence and authority fields.
- `config/labels.json`: label data, not proof labels have been applied remotely.
- `workflow-templates/`: opt-in workflow templates, not workflows active here.

For Issue forms check YAML shape, unique field IDs and public-safe prompts;
verify organization Issue Types against live GitHub when changing type bindings.
For workflow templates inspect permissions, pinned action references and event
handling; keep the adjacent properties file consistent. Do not apply templates,
labels or settings to other repositories as an incidental effect.

Run toolkit/JSON/YAML checks and inspect the rendered Markdown or form semantics
relevant to the edit. Follow the Git/GitHub contract for delivery. If acceptance
requires a live GitHub surface, inspect it after merge rather than equating a
valid file with a verified UI. Report any unavailable rendering separately.

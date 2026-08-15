# Security policy

Mind Seed has no public supported software release at this time. This policy
covers repository and organization infrastructure without claiming an
operational security support window for the private core system.

## Report privately

Do **not** disclose suspected vulnerabilities, credentials, private repository
content, personal data, protected-vault content, or working exploit material in
an issue, discussion, pull request, commit, or public log.

- For this public `.github` repository, use GitHub's
  [private vulnerability report](https://github.com/mind-seed-systems/.github/security/advisories/new)
  when the **Report a vulnerability** control is available.
- For a private organization repository, authorized collaborators should use a
  draft GitHub Security Advisory or an existing verified private channel with
  the organization owner.
- If neither private route is available, report only that a private contact is
  needed; do not include vulnerability details in the public request.

No email address or response-time promise is fabricated here. A repository that
reaches a public release boundary must publish and test a durable private
contact before release.

## Include safely

Use synthetic data and provide, where possible:

- affected repository, exact commit/version, and configuration identity;
- boundary involved: source, package, host, provider, connector, data, or
  organization infrastructure;
- minimal reproduction and expected versus observed behavior;
- impact, required authority, and whether an external effect occurred;
- redacted evidence and checksums, never secret values.

## Baseline expectations

- Local-first and least-authority defaults.
- Explicit repository/workspace grants; visibility is not authorization.
- Model, tool, issue, and pull-request content is untrusted input.
- Secrets stay outside source, prompts, command lines, logs, evidence, and
  durable memory.
- GitHub Actions receive read-only `GITHUB_TOKEN` permissions unless a reviewed
  task proves a narrower write permission is necessary.
- Third-party Actions are pinned to immutable commit SHAs.
- Pause, revocation, rollback, recovery, and removal do not depend on model
  cooperation.

Security advisories are coordinated privately. Publication timing, affected
versions, fixes, credential rotation, and disclosure scope require explicit
maintainer approval.

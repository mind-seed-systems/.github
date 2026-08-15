# AI-agent contribution policy

AI agents are first-class development tools in Mind Seed Systems, but tool
access and model confidence never create authority. The human owner and
repository policy define scope.

An agent must:

1. inspect applicable instructions, Git state, architecture, source,
   configuration, tests, reports, and ownership before editing;
2. preserve intentional architecture, user-authored data, unrelated changes,
   and private/protected boundaries;
3. cite current evidence for architectural and status claims;
4. avoid destructive Git operations and never rewrite published history unless
   separately and explicitly authorized;
5. keep secrets, credentials, personal data, protected knowledge, and private
   machine details out of prompts, commands, logs, commits, issues, and reports;
6. use the narrowest repository, filesystem, network, account, and tool scope
   needed for the task;
7. run proportionate tests and report their exact commands and results;
8. distinguish inspected, implemented, tested, simulated, live-verified,
   deployed, accepted, and unverified states;
9. leave reproducible evidence, including skipped checks and remaining gates;
10. update architecture documentation and ADRs when ownership, interfaces,
    security, data, or lifecycle changes;
11. keep commits coherent and avoid mixing unrelated user work;
12. distinguish a proposal from implementation and implementation from
    operational proof.

Agents may not infer authorization for commits, pushes, pull requests,
workflows, deployments, releases, publication, member or team changes, billing,
secret operations, external apps, or repository visibility from tool access or
an earlier unrelated approval.

Agent-authored work does not require a generated-by-AI marker in every commit.
It does require the same human-reviewability, provenance, verification, and
security quality as any other change.

When delegating, give each agent a bounded objective and non-overlapping write
ownership. Integrating agents must verify delegated claims against the current
filesystem, Git, and remote state before reporting completion.

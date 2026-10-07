# Git and GitHub workflow

Read authorization before mutations. Inspect status, diff, branch, worktrees,
remotes and upstream. Fetch `origin --prune` and inspect the target-relative diff.
Use a short-lived `codex/` branch; use an isolated worktree when existing work
would otherwise overlap. No blanket staging, destructive synchronization or
protected-history rewrite. Never stash unrelated changes for convenience.

Inspect live matching Issues/PRs before creating work objects. Read relevant
checks, reviews, rulesets/protection, Projects, tags/releases and workflow triggers.
Do not duplicate a work object. Do not infer absent Project data from a partial
or unauthorized response. Work-management state is not policy.

Prefer fast-forward synchronization. If branches diverge, inspect both sides and
use a reviewed merge or rebase appropriate to branch ownership. Rebase only
unshared task-owned commits unless express authority covers shared history.
Force pushes need express valid authority, current-state safeguards and a lease;
never force-push a protected branch or bypass protections.

Stage only reviewed task paths. Use a concise imperative commit subject aligned
with local history (for example `agent: add repository workflows`). Do not add
unsolicited attribution trailers. Push the task branch and create/update a PR
using [.github/pull_request_template.md](../../.github/pull_request_template.md).
Name the actual executor and authority in GitHub text; keep private context out.
Start as draft unless the task/configured workflow calls for a ready PR. Mark
ready after review and relevant validation; the owner's requested merge endpoint
covers this transition for completed work.

Inspect current head checks and reviews; remediate task-caused failures. Do not
claim a historical check passed at the new head. Satisfy all externally required
checks/reviews before merge. An unrelated non-required failure may be recorded
with its existing Issue and evidence; it is not a check bypass or a green result.
Choose a merge method permitted by the repository. Use head-SHA matching; never
use an admin override. Re-fetch if the head or base changed, and revalidate as
needed. Verify the resulting remote default branch contains the intended change
and inspect post-merge checks. Fast-forward a clean local default checkout when
safe. Report exact commit/PR state and remaining failures separately.

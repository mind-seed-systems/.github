# Deterministic hooks

The shared implementation is `scripts/validate_agent_toolkit.py`, invoked manually
or by `.github/workflows/agent-toolkit.yml` on pull requests and pushes to main.
It reads toolkit metadata, skills, adapters, routing cases and local links; it
also parses tracked JSON/YAML configuration. Inputs are repository files; no
network, credentials or external writes are needed. It is idempotent and normally
runs within seconds. Dependencies are Python 3 and PyYAML. Exit 0 means structural
checks passed; exit 1 means invalid input, and missing runtime/dependencies are
an unavailable check, not success. Diagnostics identify the failing path.

Manual invocation: `python3 scripts/validate_agent_toolkit.py` from the root.
Regression tests: `python3 -m unittest discover -s tests -v`.
No Git hook or provider hook is installed automatically. CI shares this single
implementation. Architecture, disclosure review, routing judgment and completion
remain reasoning tasks; this hook cannot approve them.

# Research provenance convention

Mind Seed architecture is research-driven. Important claims that affect a
decision, security boundary, compatibility contract, or implementation choice
should carry enough provenance to be checked without turning every README
sentence into an academic paper.

Use a compact record in the owning document, ADR, issue, or report:

```text
Source: stable title and URL or repository/revision
Source type: primary documentation | paper | standard | source inspection | experiment | secondary analysis
Publication date: YYYY-MM-DD or unknown
Retrieved: YYYY-MM-DD when the source can change
Claim supported: one bounded claim
Confidence: high | medium | low
Implementation consequence: decision, constraint, test, or no immediate change
Limitations: conflicting evidence, scope, or applicability
```

Prefer primary sources: official documentation and standards, original papers,
and directly inspected source or runtime evidence. A source's authority for one
claim does not make all of its recommendations project requirements.

For experiments, also record the exact source revision, authorized environment
and data, procedure, positive and negative cases, stop conditions, outputs,
evidence class, and claims still forbidden after success.

Changing web pages should include a retrieval date. Repository evidence should
include an immutable commit or artifact digest where practical. Private sources
may be described with a stable internal reference; do not copy protected
content into a public citation.

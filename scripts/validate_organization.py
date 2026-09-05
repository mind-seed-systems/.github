#!/usr/bin/env python3
"""Validate the public Mind Seed Systems organization foundation.

The validator is deliberately read-only. With pinned jsonschema it validates the
organization manifest's semantic invariants, JSON inputs, label definitions,
ADR metadata, relative Markdown links, and immutable GitHub Action references.
GitHub YAML is parsed separately by the validation workflow with Ruby's standard
YAML library.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import unicodedata
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "mind-seed-organization.json"
SCHEMA_PATH = ROOT / "schemas" / "mind-seed-organization.schema.json"
LABELS_PATH = ROOT / "config" / "labels.json"

RELATIONSHIP_TYPES = {
    "contains",
    "depends-on",
    "integrates-with",
    "implements",
    "extends",
    "provides-interface-for",
    "research-supports",
    "deployed-by",
    "supersedes",
    "related-to",
}
PROFILES = {"core", "infrastructure", "platform"}
REQUIRED_LABELS = {
    "type:bug",
    "type:feature",
    "type:architecture",
    "type:research",
    "type:documentation",
    "type:security",
    "type:refactor",
    "type:test",
    "type:chore",
    "priority:P0",
    "priority:P1",
    "priority:P2",
    "priority:P3",
    "state:blocked",
    "state:needs-decision",
    "state:ready",
    "state:in-progress",
    "breaking-change",
    "dependencies",
    "performance",
    "privacy",
}
ADR_STATUSES = {"proposed", "accepted", "deprecated", "superseded", "rejected"}
LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
ACTION_PATTERN = re.compile(r"^\s*-?\s*uses:\s*([^\s#]+)", re.MULTILINE)
IMMUTABLE_ACTION_PATTERN = re.compile(r"^[^@\s]+@[0-9a-fA-F]{40}$")
ADR_FIELD_PATTERN = re.compile(r"^(id|title|status|date|superseded_by):\s*(.*?)\s*$", re.MULTILINE)


class ValidationError(RuntimeError):
    """Raised for a deterministic organization-foundation validation error."""


def load_json(path: Path) -> object:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValidationError(f"cannot parse JSON {path.relative_to(ROOT)}: {exc}") from exc


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def unique_values(records: list[dict[str, object]], key: str, label: str) -> set[str]:
    values = [str(record.get(key, "")) for record in records]
    require(all(values), f"{label} contains an empty {key}")
    require(len(values) == len(set(values)), f"{label} contains duplicate {key} values")
    return set(values)


def markdown_fragments(path: Path) -> set[str]:
    """GitHub-style slugs for the repository's ATX headings, including duplicates."""
    fragments: set[str] = set()
    fence = None
    for line in path.read_text(encoding="utf-8").splitlines():
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence is not None:
            continue
        heading = re.match(r"^ {0,3}#{1,6}\s+(.+?)(?:\s+#+)?\s*$", line)
        if not heading:
            continue
        text = re.sub(r"<[^>]*>", "", heading.group(1)).lower()
        text = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", text)
        slug = "".join(c for c in text if c in "-_ " or unicodedata.category(c)[0] in "LN").replace(" ", "-")
        candidate, suffix = slug, 0
        while candidate in fragments:
            suffix += 1
            candidate = f"{slug}-{suffix}"
        fragments.add(candidate)
    return fragments


def validate_fragment(path: Path, fragment: str) -> None:
    if fragment and path.suffix.lower() == ".md":
        require(unquote(fragment) in markdown_fragments(path),
                f"unknown Markdown fragment: {path.relative_to(ROOT)}#{fragment}")


def validate_reference(reference: str, *, local: bool) -> None:
    """Manifest references are canonical repository-relative paths, never URLs."""
    split = urlsplit(reference)
    path_text = unquote(split.path)
    require(not split.scheme and not split.netloc and not split.query and path_text
            and not path_text.startswith("/") and "\\" not in path_text
            and not any(ord(c) < 32 or ord(c) == 127 for c in reference + path_text)
            and all(part not in {"", ".", ".."} for part in path_text.split("/")),
            f"unsafe repository-relative reference: {reference}")
    if local:
        path = (ROOT / path_text).resolve()
        require(path.is_relative_to(ROOT.resolve()), f"reference escapes repository: {reference}")
        require(path.is_file(), f"reference does not exist: {reference}")
        validate_fragment(path, split.fragment)


def validate_live_inventory(manifest: dict) -> None:
    """Explicitly opted-in authenticated GETs; no content or settings are requested."""
    try:
        subprocess.run(["gh", "auth", "status", "--hostname", "github.com"],
                       check=True, capture_output=True, text=True, timeout=30)
        result = subprocess.run(
            ["gh", "api", "--hostname", "github.com", "--method", "GET", "--paginate", "--slurp",
             "orgs/mind-seed-systems/repos?type=all&per_page=100"],
            check=True, capture_output=True, text=True, timeout=60)
        live = [repository for page in json.loads(result.stdout) for repository in page]
    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        raise ValidationError("live inventory unavailable: authenticated gh with organization/private-repository read access required") from exc
    expected = {r["name"]: (r["visibility"], r["defaultBranch"]) for r in manifest["repositories"]}
    actual = {r["name"]: (r["visibility"], r["default_branch"]) for r in live}
    require(actual == expected,
            "live inventory mismatch (or incomplete private-repository access): "
            f"missing={sorted(expected.keys() - actual.keys())}, "
            f"extra={sorted(actual.keys() - expected.keys())}, "
            f"changed={sorted(k for k in expected.keys() & actual.keys() if expected[k] != actual[k])}")
    print("authenticated read-only live inventory matches names, visibility, and default branches")


def validate_manifest(manifest: dict | None = None) -> tuple[int, int, int]:
    if manifest is None:
        manifest = load_json(MANIFEST_PATH)
    schema = load_json(SCHEMA_PATH)
    try:
        from jsonschema import Draft202012Validator, FormatChecker
    except ImportError as exc:
        raise ValidationError("install scripts/requirements-validation.txt before validation") from exc
    Draft202012Validator.check_schema(schema)
    errors = sorted(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(manifest),
                    key=lambda error: str(list(error.absolute_path)))
    require(not errors, "JSON Schema: " + "; ".join(
        f"{list(error.absolute_path)}: {error.message}" for error in errors))
    require(isinstance(manifest, dict), "organization manifest must be an object")
    require(isinstance(schema, dict), "organization schema must be an object")
    require(manifest.get("$schema") == "./schemas/mind-seed-organization.schema.json", "manifest $schema path is not canonical")
    require(manifest.get("schemaVersion") == "mind-seed.organization/v1", "unsupported organization manifest version")

    organization = manifest.get("organization")
    require(isinstance(organization, dict), "manifest organization must be an object")
    require(organization.get("id") == "mind-seed-systems", "organization id must be mind-seed-systems")
    require(organization.get("displayName") == "Mind Seed Systems", "organization display name is incorrect")
    require(organization.get("coreProject") == "Mind Seed", "core project must be Mind Seed")
    require(organization.get("visibilityPolicy") == "private-by-default", "visibility policy must remain private-by-default")

    repositories = manifest.get("repositories")
    require(isinstance(repositories, list) and repositories, "manifest must contain repositories")
    require(all(isinstance(item, dict) for item in repositories), "repository entries must be objects")
    repository_ids = unique_values(repositories, "id", "repositories")
    repository_names = unique_values(repositories, "name", "repositories")
    require(sum(item["role"] == "organization-infrastructure" for item in repositories) == 1,
            "exactly one organization infrastructure repository is required")
    require(any(item["name"] == ".github" and item["role"] == "organization-infrastructure"
                for item in repositories), ".github must own organization infrastructure")
    require(any(item["name"] == "Mind-Seed" and item["role"] == "canonical-core"
                for item in repositories), "Mind-Seed must be the canonical core")
    require(sum(item.get("role") == "canonical-core" for item in repositories) == 1, "exactly one canonical core is required")
    require(all(item.get("defaultBranch") == "main" for item in repositories), "every repository default branch must be main")

    require(organization["githubUrl"] == "https://github.com/mind-seed-systems",
            "organization URL does not match identity")
    require(organization["repositoryNamePattern"] == "mind-seed-<component>", "future naming pattern drifted")
    require(set(organization["preservedRepositoryNames"]) <= repository_names,
            "preserved repository name has no repository")
    for repository in repositories:
        name = repository["name"]
        require(re.fullmatch(r"[A-Za-z0-9_.-]+", name) is not None and name not in {".", ".."},
                "invalid repository name")
        require(name in organization["preservedRepositoryNames"] or
                re.fullmatch(r"mind-seed-[a-z0-9]+(?:-[a-z0-9]+)*", name) is not None,
                f"repository name violates naming policy: {name}")
        require(repository["url"] == f"https://github.com/mind-seed-systems/{name}",
                f"repository URL does not match identity: {name}")
        owners = repository.get("owners")
        require(isinstance(owners, list) and owners, f"repository {repository['id']} must have an owner")
        require(all(re.fullmatch(r"@[A-Za-z0-9-]+", str(owner)) for owner in owners), f"repository {repository['id']} has an invalid owner")
        docs = repository.get("documentation")
        require(isinstance(docs, list) and docs, f"repository {repository['id']} must have documentation")
        for reference in docs:
            require(isinstance(reference, dict), "documentation references must be objects")
            require(reference["repository"] in repository_names, "unknown documentation repository")
            validate_reference(reference["path"], local=reference["repository"] == ".github")

    components = manifest.get("componentDomains")
    require(isinstance(components, list), "componentDomains must be a list")
    unique_values(components, "id", "componentDomains")
    for component in components:
        require(component.get("currentOwner") in repository_ids, f"component {component.get('id')} has unknown owner")
        if component["boundary"] == "current-core":
            require(any(repo["id"] == component["currentOwner"] and repo["role"] == "canonical-core"
                        for repo in repositories), "current-core domain must belong to canonical core")

    externals = manifest.get("externalEntities")
    require(isinstance(externals, list), "externalEntities must be a list")
    external_ids = unique_values(externals, "id", "externalEntities") if externals else set()
    require(repository_ids.isdisjoint(external_ids), "repository and external entity IDs overlap")

    relationship_types = manifest.get("relationshipTypes")
    require(isinstance(relationship_types, list), "relationshipTypes must be a list")
    require(set(relationship_types) == RELATIONSHIP_TYPES, "relationship type vocabulary drifted")

    relationships = manifest.get("relationships")
    require(isinstance(relationships, list), "relationships must be a list")
    known_entities = repository_ids | external_ids
    seen_edges: set[tuple[str, str, str]] = set()
    for edge in relationships:
        require(isinstance(edge, dict), "relationship entries must be objects")
        source = str(edge.get("source", ""))
        target = str(edge.get("target", ""))
        edge_type = str(edge.get("type", ""))
        require(source in known_entities, f"relationship has unknown source: {source}")
        require(target in known_entities, f"relationship has unknown target: {target}")
        require(edge_type in RELATIONSHIP_TYPES, f"relationship has unknown type: {edge_type}")
        identity = (source, edge_type, target)
        require(identity not in seen_edges, f"duplicate relationship: {identity}")
        seen_edges.add(identity)
        validate_reference(edge["evidence"], local=True)

    return len(repositories), len(components), len(relationships)


def validate_labels() -> int:
    config = load_json(LABELS_PATH)
    require(isinstance(config, dict), "label config must be an object")
    require(config.get("schemaVersion") == "mind-seed.labels/v1", "unsupported label config version")
    require(set(config.get("profiles", [])) == PROFILES, "label profile vocabulary drifted")
    labels = config.get("labels")
    require(isinstance(labels, list) and labels, "label config must contain labels")
    names = unique_values(labels, "name", "labels")
    require(REQUIRED_LABELS <= names, f"required labels missing: {sorted(REQUIRED_LABELS - names)}")
    for label in labels:
        require(re.fullmatch(r"[0-9A-Fa-f]{6}", str(label.get("color", ""))) is not None, f"label {label.get('name')} has invalid color")
        require(bool(str(label.get("description", "")).strip()), f"label {label.get('name')} has no description")
        label_profiles = set(label.get("profiles", []))
        require(label_profiles and label_profiles <= PROFILES, f"label {label.get('name')} has invalid profiles")
    defaults = config.get("githubDefaultsToRemove")
    require(isinstance(defaults, list) and len(defaults) == len(set(defaults)), "GitHub default removal list is invalid")
    return len(labels)


def validate_adrs() -> int:
    paths = sorted((ROOT / "docs" / "architecture" / "decisions").glob("ADR-*.md"))
    require(paths, "at least one organization ADR is required")
    seen_ids: set[str] = set()
    for path in paths:
        text = path.read_text(encoding="utf-8")
        require(text.startswith("---\n"), f"ADR lacks YAML front matter: {path.relative_to(ROOT)}")
        try:
            front_matter = text.split("---\n", 2)[1]
        except IndexError as exc:
            raise ValidationError(f"ADR front matter is not closed: {path.relative_to(ROOT)}") from exc
        fields = dict(ADR_FIELD_PATTERN.findall(front_matter))
        required = {"id", "title", "status", "date", "superseded_by"}
        require(required <= fields.keys(), f"ADR is missing metadata fields: {path.relative_to(ROOT)}")
        adr_id = fields["id"]
        require(re.fullmatch(r"ADR-[0-9]{4}", adr_id) is not None, f"ADR has invalid id: {adr_id}")
        require(adr_id not in seen_ids, f"duplicate ADR id: {adr_id}")
        seen_ids.add(adr_id)
        require(fields["status"] in ADR_STATUSES, f"ADR has invalid status: {path.relative_to(ROOT)}")
        require(re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", fields["date"]) is not None, f"ADR has invalid date: {path.relative_to(ROOT)}")
        for heading in (
            "## Context",
            "## Decision",
            "## Alternatives considered",
            "## Consequences",
            "## Dependencies",
            "## Supersession",
            "## Evidence and verification",
        ):
            require(heading in text, f"ADR lacks {heading}: {path.relative_to(ROOT)}")
    return len(paths)


def resolve_markdown_target(source: Path, raw_target: str) -> Path | None:
    target = raw_target.strip().strip("<>")
    public_prefix = "https://github.com/mind-seed-systems/.github/blob/main/"
    if target.startswith(public_prefix):
        reference = target[len(public_prefix):]
        validate_reference(reference, local=True)
        return (ROOT / unquote(urlsplit(reference).path)).resolve()
    if not target:
        return None
    split = urlsplit(target)
    if split.scheme or split.netloc:
        return None
    path_text = unquote(split.path)
    if not path_text:
        return source
    return (source.parent / path_text).resolve()


def validate_markdown_links() -> tuple[int, int]:
    markdown_paths = sorted(path for path in ROOT.rglob("*.md") if ".git" not in path.parts)
    link_count = 0
    for path in markdown_paths:
        text = path.read_text(encoding="utf-8")
        for match in LINK_PATTERN.finditer(text):
            target = resolve_markdown_target(path, match.group(1))
            if target is None:
                continue
            link_count += 1
            try:
                target.relative_to(ROOT)
            except ValueError as exc:
                raise ValidationError(f"relative link escapes repository: {path.relative_to(ROOT)} -> {match.group(1)}") from exc
            require(target.exists(), f"broken relative link: {path.relative_to(ROOT)} -> {match.group(1)}")
            validate_fragment(target, urlsplit(match.group(1).strip().strip("<>")).fragment)
    return len(markdown_paths), link_count


def validate_action_pins() -> int:
    yaml_paths = sorted((ROOT / ".github" / "workflows").glob("*.yml")) + sorted((ROOT / "workflow-templates").glob("*.yml"))
    reference_count = 0
    for path in yaml_paths:
        text = path.read_text(encoding="utf-8")
        for reference in ACTION_PATTERN.findall(text):
            reference_count += 1
            require(IMMUTABLE_ACTION_PATTERN.fullmatch(reference) is not None, f"Action is not pinned to a full commit SHA: {path.relative_to(ROOT)} -> {reference}")
        require("permissions:" in text and "contents: read" in text, f"workflow lacks explicit read-only content permission: {path.relative_to(ROOT)}")
    require(reference_count > 0, "no pinned Action references found")
    return reference_count


def validate_all_json() -> int:
    paths = sorted(path for path in ROOT.rglob("*.json") if ".git" not in path.parts)
    for path in paths:
        load_json(path)
    return len(paths)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live-inventory", action="store_true",
                        help="explicit authenticated read-only reconciliation against GitHub")
    args = parser.parse_args()
    try:
        repositories, components, relationships = validate_manifest()
        labels = validate_labels()
        adrs = validate_adrs()
        markdown_files, links = validate_markdown_links()
        action_references = validate_action_pins()
        json_files = validate_all_json()
        if args.live_inventory:
            validate_live_inventory(load_json(MANIFEST_PATH))
    except ValidationError as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        return 1

    print(
        "organization foundation valid: "
        f"{repositories} repositories, {components} component domains, "
        f"{relationships} relationships, {labels} labels, {adrs} ADRs, "
        f"{markdown_files} Markdown files, {links} relative links, "
        f"{action_references} pinned Action references, {json_files} JSON files"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

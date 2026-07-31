#!/usr/bin/env python3
"""Validate the Atlas catalog using only the Python standard library."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "papers.json"

REQUIRED = {
    "id", "title", "year", "authors", "venue", "publication_status",
    "study_type", "url", "code_url", "specification", "representation",
    "allocation", "placement", "rejected_behavior", "guarantees",
    "systems_measurements", "outcome_measurements", "review_status",
    "evidence_note",
}

VOCAB = {
    "publication_status": {"peer_reviewed", "preprint", "documentation", "other"},
    "review_status": {"metadata_verified", "full_text_screened", "full_text_coded", "second_pass_verified"},
    "specification": {"lexical", "syntax", "schema", "type", "semantic", "relation", "state", "policy"},
    "representation": {"regex_fsm", "cfg_parser", "pda", "trie", "token_index", "programmatic", "solver", "classifier", "membership_oracle", "provider_undisclosed", "framework_dependent"},
    "allocation": {"local_masking", "beam_search", "lookahead", "rejection_sampling", "importance_weighting", "sequential_monte_carlo", "draft_conditioning", "speculative", "retry", "deterministic_validation", "framework_dependent"},
    "placement": {"token", "field", "sequence", "action_boundary", "commit", "multi_stage"},
    "rejected_behavior": {"mask", "prune", "resample", "regenerate", "repair", "reject", "fallback", "confirm", "not_applicable", "not_reported"},
    "guarantees": {"language_soundness", "token_reachable_coverage", "termination", "totality", "distribution_fidelity", "semantic_correctness", "state_validity", "freshness", "authorization", "external_effect_safety", "not_reported"},
    "systems_measurements": {"compile_time", "plan_memory", "host_memory", "device_memory", "latency", "tpot", "throughput", "batch_scaling", "cache_behavior", "end_to_end_cost", "not_reported"},
    "outcome_measurements": {"format_validity", "schema_coverage", "task_accuracy", "execution_accuracy", "distribution_divergence", "abstention", "external_state_effect", "user_outcome", "not_reported"},
}


def valid_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def main() -> int:
    rows = json.loads(CATALOG.read_text())
    errors: list[str] = []
    ids: set[str] = set()
    titles: set[str] = set()
    urls: set[str] = set()

    if not isinstance(rows, list):
        print("catalog root must be a list", file=sys.stderr)
        return 1

    for index, row in enumerate(rows):
        label = row.get("id", f"row-{index}") if isinstance(row, dict) else f"row-{index}"
        if not isinstance(row, dict):
            errors.append(f"{label}: record must be an object")
            continue

        missing = REQUIRED - row.keys()
        extra = row.keys() - REQUIRED
        if missing:
            errors.append(f"{label}: missing fields {sorted(missing)}")
        if extra:
            errors.append(f"{label}: unknown fields {sorted(extra)}")

        for field in ("id", "title", "venue", "url", "evidence_note"):
            if not isinstance(row.get(field), str) or not row[field].strip():
                errors.append(f"{label}: {field} must be a non-empty string")

        if not isinstance(row.get("year"), int) or not 1950 <= row["year"] <= 2100:
            errors.append(f"{label}: invalid year")
        if not isinstance(row.get("authors"), list) or not row["authors"] or not all(isinstance(x, str) and x.strip() for x in row["authors"]):
            errors.append(f"{label}: authors must be a non-empty string list")
        if isinstance(row.get("url"), str) and not valid_url(row["url"]):
            errors.append(f"{label}: invalid url {row['url']!r}")
        if row.get("code_url") is not None and (not isinstance(row["code_url"], str) or not valid_url(row["code_url"])):
            errors.append(f"{label}: invalid code_url")

        for field, allowed in VOCAB.items():
            value = row.get(field)
            values = [value] if field in {"publication_status", "review_status"} else value
            if not isinstance(values, list) or not values:
                errors.append(f"{label}: {field} must be non-empty")
                continue
            unknown = set(values) - allowed
            if unknown:
                errors.append(f"{label}: unknown {field} labels {sorted(unknown)}")
            if len(values) != len(set(values)):
                errors.append(f"{label}: duplicate {field} labels")

        normalized_title = " ".join(row.get("title", "").lower().split())
        for field, value, seen in (("id", row.get("id"), ids), ("title", normalized_title, titles), ("url", row.get("url"), urls)):
            if value in seen:
                errors.append(f"{label}: duplicate {field} {value!r}")
            seen.add(value)

    if errors:
        print("Catalog validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Catalog valid: {len(rows)} records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

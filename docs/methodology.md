# Corpus and Coding Methodology

## Scope

The Atlas covers methods, systems, analyses, benchmarks, applications, and
adjacent enforcement work that materially constrain, validate, repair, or
condition language-model outputs. It includes token-time constrained decoding
as well as later lifecycle placements when they are necessary for a meaningful
comparison of guarantees.

The Atlas is a **curated public resource**, not a systematic-review claim.
Counts describe this catalog snapshot and must not be interpreted as field-wide
prevalence.

## Discovery

The initial corpus was assembled on 2026-07-31 from:

- arXiv title/abstract searches;
- ACL Anthology and PMLR venue searches;
- backward references from pivotal papers;
- forward citation and author-page checks where available; and
- community lists used for recall only, never as evidence for coding.

The initial query families are recorded in [`data/search-log.tsv`](../data/search-log.tsv).
Discovery is deliberately broad. Inclusion and taxonomy coding are separate
steps.

## Inclusion

A work is in scope when constrained language-model generation or a directly
comparable enforcement mechanism is load-bearing to at least one of:

- the method;
- a formal guarantee;
- a systems contribution;
- an evaluation protocol; or
- an external-action safety claim.

Pure prompting papers, generic decoding papers without an executable
constraint, and application papers that merely consume an unrelated structured
output API are excluded. Borderline runtime-enforcement work may be retained as
`adjacent_enforcement` and must be visibly labeled.

## Evidence workflow

Records move monotonically through four states:

1. `metadata_verified`: bibliographic identity and stable link checked;
2. `full_text_screened`: inclusion decision checked against the paper;
3. `full_text_coded`: every load-bearing label checked from full text;
4. `second_pass_verified`: coding independently rechecked after vocabulary
   stabilization.

Metadata-only records improve discovery but are excluded from strong synthesis.
An absent measurement is `not_reported`, never zero. A guarantee is not inferred
from an implementation family or empirical success.

## Coding unit and disagreement policy

The unit is a distinct work, preferring the archival version over duplicate
preprints. Multi-component systems may receive multiple labels on each axis.
When evidence is ambiguous, the narrower label wins until the primary source
licenses a stronger one. Corrections preserve the public history through issues,
pull requests, and release snapshots.

## Reproducibility

The source of truth is [`data/papers.json`](../data/papers.json). The schema and
standard-library validator reject missing fields, uncontrolled labels, duplicate
records, malformed URLs, and contradictory `not_reported` mixtures. Human-readable
views and the website are generated from that same file.

```bash
python3 scripts/validate_catalog.py
python3 scripts/generate_views.py
python3 scripts/generate_site.py
```

## Known limitations

- The discovery process is not yet exhaustive.
- Nearly half of the current records remain metadata-verified rather than
  fully coded.
- Guarantee evidence strength is not yet stored per property.
- Provider features and software versions change faster than paper metadata;
  an independently dated capability table is deferred until provenance rules
  are stable.

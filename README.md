# Constrained Decoding Atlas

[![Catalog](https://img.shields.io/badge/catalog-49%20papers-58e1d5)](https://rainiver.github.io/constrained-decoding-atlas/)
[![Validate](https://github.com/Rainiver/constrained-decoding-atlas/actions/workflows/validate.yml/badge.svg)](https://github.com/Rainiver/constrained-decoding-atlas/actions/workflows/validate.yml)
[![Pages](https://github.com/Rainiver/constrained-decoding-atlas/actions/workflows/pages.yml/badge.svg)](https://rainiver.github.io/constrained-decoding-atlas/)
[![License: CC BY 4.0](https://img.shields.io/badge/data%20%26%20docs-CC%20BY%204.0-ae8cff)](DATA_LICENSE.md)

> An evidence-coded map of constrained generation, structured output, and
> runtime enforcement for language models.

**Status:** public preview `v0.1`. The Atlas currently indexes 49 heterogeneous
works. Coverage is intentionally transparent rather than presented as a
complete or systematic census; 40 discovery records still await full-text
coding.

## Why another repository?

Awesome lists answer **what exists**. This Atlas is designed to answer:

- What kind of constraint is specified?
- How is it represented and executed?
- How does it change decoding or search?
- Where in the generation-to-commit lifecycle does it act?
- What does it actually guarantee—and under which assumptions?
- Which compile, memory, latency, quality, and downstream effects were measured?
- Which claims were checked from full text rather than inferred from titles?

Every record follows a controlled taxonomy and carries an evidence status.
Missing measurements are recorded as `not_reported`, never as zero.

## Browse the Atlas

- [Interactive website](https://rainiver.github.io/constrained-decoding-atlas/)
- [Taxonomy](docs/taxonomy.md)
- [Guarantees: what the labels mean](docs/guarantees.md)
- [Practitioner decision guide](docs/decision-guide.md)
- [Generated catalog](docs/catalog.md)
- [Evidence coverage snapshot](docs/coverage.md)
- [Corpus and coding methodology](docs/methodology.md)
- [Machine-readable paper catalog](data/papers.json)
- [Contribution guide](CONTRIBUTING.md)
- [Roadmap](ROADMAP.md)

## The seven views

| View | Questions encoded |
|---|---|
| Specification | lexical, syntax, schema, type, semantic, relation, state, policy |
| Representation | regex/FSM, CFG/parser, trie, token index, program, solver, oracle |
| Allocation | local mask, lookahead, rejection, SMC, beam/search, draft, retry, validation |
| Placement | token, field/span, completed sequence, action boundary, commit |
| Guarantees | soundness, token coverage, totality, distribution, semantics, freshness, authorization |
| Systems | compile time, memory, latency, throughput, batching, cache behavior |
| Evaluation | format, task quality, distribution, external effects, reproducibility |

## What this repository is not

- It is not currently a claim to be the first survey of constrained
  generation. A peer-reviewed TMLR survey already exists.
- It does not rank systems using incomparable numbers.
- It does not treat an unreported metric as a failed metric.
- It does not copy paper abstracts; summaries and coding notes must be original.
- It is not the archival contribution of any associated empirical paper.

## Validate locally

```bash
python3 scripts/validate_catalog.py
```

The same check runs on every pull request.

## License

- Validation and generation code: [MIT](LICENSE).
- Original catalog annotations and documentation: [CC BY 4.0](DATA_LICENSE.md).
- Paper titles, author names, venue metadata, and outbound links remain
  bibliographic facts or third-party material; this repository does not
  redistribute paper text.

## Current release target

Release `v0.1` contains 49 heterogeneous records across formal-language
decoding, probabilistic constrained inference, serving systems,
structured-output benchmarks, and runtime enforcement. Evidence depth remains
visible per record: metadata-only entries are discoverable but excluded from
strong synthesis until full-text coding is complete. See the
[changelog](CHANGELOG.md) for snapshot details.

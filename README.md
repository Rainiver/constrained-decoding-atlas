# Constrained Decoding Atlas

> An evidence-coded map of constrained generation, structured output, and
> runtime enforcement for language models.

**Status:** bootstrap release. The catalog is intentionally small while the
screening protocol and taxonomy are being validated; it is not yet a
comprehensive list.

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

- [Taxonomy](docs/taxonomy.md)
- [Guarantees: what the labels mean](docs/guarantees.md)
- [Practitioner decision guide](docs/decision-guide.md)
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

## Near-term target

The first public milestone is 30 heterogeneous, full-text-coded papers across
formal-language decoding, probabilistic constrained inference, serving
systems, structured-output benchmarks, and runtime enforcement. Static views
and coverage dashboards will be generated only after the vocabulary is stable.


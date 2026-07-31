# Taxonomy

The Atlas codes methods along orthogonal dimensions. A paper may have multiple
labels on any dimension.

## 1. Constraint specification

| Label | Meaning |
|---|---|
| `lexical` | Include/exclude words, phrases, or token patterns. |
| `syntax` | Regular or context-free structural language. |
| `schema` | Data-format contract such as JSON Schema. |
| `type` | Type correctness or typed API/program constraints. |
| `semantic` | Property whose truth depends on meaning or program behavior. |
| `relation` | Constraint across two or more generated values. |
| `state` | Validity depends on mutable environment state. |
| `policy` | Authorization, safety, or organizational rule. |

## 2. Executable representation

`regex_fsm`, `cfg_parser`, `pda`, `trie`, `token_index`, `programmatic`,
`solver`, `classifier`, `membership_oracle`, `provider_undisclosed`,
`framework_dependent`.

## 3. Allocation or search

`local_masking`, `beam_search`, `lookahead`, `rejection_sampling`,
`importance_weighting`, `sequential_monte_carlo`, `draft_conditioning`,
`speculative`, `retry`, `deterministic_validation`, `framework_dependent`.

## 4. Placement

| Label | Earliest enforcement point |
|---|---|
| `token` | Each next-token decision. |
| `field` | A structured field or span boundary. |
| `sequence` | Completed text or structured object. |
| `action_boundary` | Parsed tool/action proposal before execution. |
| `commit` | Immediately before external side effects. |
| `multi_stage` | More than one distinct placement is load-bearing. |

## 5. Rejected-proposal behavior

`mask`, `prune`, `resample`, `regenerate`, `repair`, `reject`, `fallback`,
`confirm`, `not_applicable`, `not_reported`.

These labels describe mechanism behavior, not whether it is desirable.

## 6. Guarantees

`language_soundness`, `token_reachable_coverage`, `termination`, `totality`,
`distribution_fidelity`, `semantic_correctness`, `state_validity`,
`freshness`, `authorization`, `external_effect_safety`, `not_reported`.

See [guarantees.md](guarantees.md). A property is coded as a guarantee only
when the paper states its assumptions and supplies a proof or construction;
empirical success alone is a measurement.

## 7. Measurements

Systems:

`compile_time`, `plan_memory`, `host_memory`, `device_memory`, `latency`,
`tpot`, `throughput`, `batch_scaling`, `cache_behavior`, `end_to_end_cost`.

Quality and outcomes:

`format_validity`, `schema_coverage`, `task_accuracy`, `execution_accuracy`,
`distribution_divergence`, `abstention`, `external_state_effect`,
`user_outcome`, `not_reported`.

## Coding rule

Do not infer a guarantee from an implementation family. For example, using a
CFG parser may support language soundness, but the record receives that label
only if the complete tokenizer/parser integration and assumptions are stated.


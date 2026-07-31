# Practitioner Decision Guide

This guide is intentionally conservative while the Atlas is in bootstrap.

## Start with the required property

1. **Only machine-parseable structure is required.** Compare schema coverage,
   tokenizer integration, latency, and batching. Do not infer semantic safety.
2. **A finite semantic set must be enforced.** Record who constructs the set,
   its freshness, cardinality, and what happens when the desired value is not
   present.
3. **Values depend on one another.** Verify that the system supports the joint
   relation rather than independent field-wise filtering.
4. **The output causes side effects.** Add action-boundary validation and make
   rejected-proposal behavior explicit; syntax enforcement alone is not an
   authorization mechanism.
5. **Sampling distribution matters.** Require an explicit distributional
   target and supporting analysis; local masking is not automatically exact
   sequence conditioning.

## Minimum evaluation card

For any deployment, record:

- schema/language and unsupported features;
- tokenizer and model revision;
- constraint construction source and timestamp;
- compile/plan memory and warmed latency/throughput;
- structural validity and semantic/task correctness separately;
- fallback/retry behavior;
- complete external state diff for mutating actions;
- versioned artifacts and reproducible prompts.

The final guide will link each recommendation to coded evidence rather than
presenting it as universal advice.


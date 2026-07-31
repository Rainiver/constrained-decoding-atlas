# Guarantee Glossary

Constraint systems are often compared using the word “guarantee” while
referring to different objects. The Atlas keeps them separate.

## Language soundness

Every emitted completed string belongs to the declared language. This does
not imply that all declared strings are token-reachable, likely, useful, or
semantically correct.

## Token-reachable coverage

Every intended valid string has at least one realizable path through the
model tokenizer and constraint implementation. This is distinct from language
soundness.

## Termination and totality

Termination says the procedure finishes under stated assumptions. Totality
says every input has an admitted outcome, which may require a fallback.

## Distribution fidelity

The constrained sampler follows a precisely named target distribution, often
the base model conditioned on a constraint. Local masking and renormalization
must not be assumed to provide sequence-level conditioning.

## Semantic correctness

The generated result is correct for the task, not merely well formed.
Structural validity is not evidence of semantic correctness.

## Type soundness

Every completed program or expression satisfies a stated type system under its
assumptions. This is stronger than grammar membership but does not by itself
imply functional correctness.

## State validity and freshness

State validity means the action satisfies a state predicate at the checked
time. Freshness records whether the predicate is re-evaluated against the
state relevant to execution.

## Authorization

The mechanism changes or commits only actions permitted by a stated authority
or repair policy. It cannot be inferred from schema validity.

## External-effect safety

Executed side effects satisfy a declared safety property. A valid tool call is
not automatically a safe world-state transition.

## Evidence levels

Each property should eventually be tagged as one of:

- `proved`;
- `by_construction`;
- `empirically_tested`;
- `claimed_only`;
- `not_reported`.

The current public-preview catalog stores the property names; evidence-level
coding is scheduled before taxonomy version 1.0.

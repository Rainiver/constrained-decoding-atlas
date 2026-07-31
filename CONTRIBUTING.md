# Contributing

Contributions are welcome, but the Atlas is evidence-coded rather than
link-only. A pull request adding a paper must update `data/papers.json` and pass
`python3 scripts/validate_catalog.py`.

For a low-friction suggestion, open the **Add a paper** issue form. Maintainers
may merge metadata-only discovery records, but strong synthesis is restricted
to full-text-coded records.

## Before adding a record

1. Prefer the archival version over a duplicate preprint.
2. Read the primary full text. Do not code a method from its title or abstract.
3. Use only controlled vocabulary from `docs/taxonomy.md`.
4. Add a section/page pointer in `evidence_note` for every load-bearing
   classification.
5. Write an original one- or two-sentence note; do not paste the abstract.
6. Use `not_reported` when a cost or outcome is absent.

## Evidence status

- `metadata_verified`: title, authors, year, venue, and URL checked.
- `full_text_screened`: inclusion criteria checked against the full text.
- `full_text_coded`: all taxonomy fields checked with evidence pointers.
- `second_pass_verified`: coding independently rechecked after the taxonomy
  stabilized.

Only `full_text_coded` and `second_pass_verified` records should be used in
evidence synthesis. The README inventory may count provisional discovery
labels, but must identify them as catalog annotations rather than field-wide
evidence.

## Pull request checklist

- [ ] Stable primary URL supplied.
- [ ] Duplicate title/arXiv/DOI checked.
- [ ] Controlled vocabulary validated.
- [ ] Publication status distinguished from preprint status.
- [ ] Claims and guarantees separated from empirical measurements.
- [ ] No copied abstract or marketing language.
- [ ] Evidence note points to the full text.

Disagreements are resolved by retaining the narrower classification until the
primary source licenses a stronger one.

## Reproduce generated views

```bash
python3 scripts/generate_views.py
python3 scripts/generate_site.py
git diff --check
```

Generated Markdown views are committed. The `site/` directory is a disposable
build artifact deployed by GitHub Actions.

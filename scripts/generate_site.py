#!/usr/bin/env python3
"""Build the dependency-free Atlas website for GitHub Pages."""

from __future__ import annotations

import json
import shutil
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"
OUT = ROOT / "site"
CATALOG = ROOT / "data" / "papers.json"


def main() -> None:
    rows = json.loads(CATALOG.read_text())
    rows.sort(key=lambda row: (-row["year"], row["title"].lower()))

    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(WEB, OUT)

    reviewed = {"full_text_screened", "full_text_coded", "second_pass_verified"}
    fully_coded = {"full_text_coded", "second_pass_verified"}
    synthesis_rows = [row for row in rows if row["review_status"] in fully_coded]
    stats = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "records": len(rows),
        "peer_reviewed": sum(row["publication_status"] == "peer_reviewed" for row in rows),
        "full_text_reviewed": sum(row["review_status"] in reviewed for row in rows),
        "fully_coded": len(synthesis_rows),
        "with_code": sum(bool(row["code_url"]) for row in rows),
        "years": dict(sorted(Counter(str(row["year"]) for row in rows).items())),
        "specification": Counter(label for row in synthesis_rows for label in row["specification"]),
        "placement": Counter(label for row in synthesis_rows for label in row["placement"]),
        "guarantees": Counter(label for row in synthesis_rows for label in row["guarantees"]),
        "systems_measurements": Counter(label for row in synthesis_rows for label in row["systems_measurements"]),
        "outcome_measurements": Counter(label for row in synthesis_rows for label in row["outcome_measurements"]),
    }

    (OUT / "catalog.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n")
    (OUT / "stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2) + "\n")
    (OUT / ".nojekyll").write_text("")
    (OUT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nSitemap: https://rainiver.github.io/constrained-decoding-atlas/sitemap.xml\n"
    )
    (OUT / "sitemap.xml").write_text(
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n"
        "  <url><loc>https://rainiver.github.io/constrained-decoding-atlas/</loc></url>\n"
        "</urlset>\n"
    )
    print(f"Built {OUT} with {len(rows)} records")


if __name__ == "__main__":
    main()

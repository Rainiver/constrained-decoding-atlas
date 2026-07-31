#!/usr/bin/env python3
"""Check the generated static site without third-party dependencies."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
CATALOG = ROOT / "data" / "papers.json"


def main() -> int:
    required = {
        "index.html", "styles.css", "app.js", "catalog.json", "stats.json",
        "robots.txt", "sitemap.xml", ".nojekyll",
    }
    missing = sorted(name for name in required if not (SITE / name).exists())
    if missing:
        raise SystemExit(f"missing site files: {', '.join(missing)}")

    source = json.loads(CATALOG.read_text())
    deployed = json.loads((SITE / "catalog.json").read_text())
    stats = json.loads((SITE / "stats.json").read_text())
    html = (SITE / "index.html").read_text()
    script = (SITE / "app.js").read_text()

    by_id = lambda rows: sorted(rows, key=lambda row: row["id"])
    assert by_id(deployed) == by_id(source), "deployed catalog differs from source catalog"
    assert stats["records"] == len(source), "stats record count is stale"
    assert stats["peer_reviewed"] == sum(row["publication_status"] == "peer_reviewed" for row in source)
    assert 'href="styles.css"' in html and 'src="app.js"' in html
    assert 'fetch("catalog.json")' in script and 'fetch("stats.json")' in script
    assert "https://rainiver.github.io/constrained-decoding-atlas/" in html
    print(f"Static site valid: {len(source)} records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

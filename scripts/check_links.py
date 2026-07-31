#!/usr/bin/env python3
"""Check catalog and README links with conservative HTTP semantics."""

from __future__ import annotations

import argparse
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "papers.json"
README = ROOT / "README.md"
REACHABLE_HTTP_ERRORS = {401, 403, 405, 429}


def probe(url: str, timeout: float) -> tuple[str, str]:
    request = Request(url, method="HEAD", headers={"User-Agent": "constrained-decoding-atlas-link-check/0.1"})
    try:
        with urlopen(request, timeout=timeout) as response:
            return url, str(response.status)
    except HTTPError as error:
        if error.code in REACHABLE_HTTP_ERRORS:
            return url, str(error.code)
        return url, f"HTTP {error.code}"
    except (URLError, TimeoutError, OSError) as error:
        return url, f"ERROR {error}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="exit nonzero when a link cannot be reached")
    parser.add_argument("--timeout", type=float, default=15.0)
    args = parser.parse_args()

    rows = json.loads(CATALOG.read_text())
    urls = {row[field] for row in rows for field in ("url", "code_url") if row.get(field)}
    urls.update(re.findall(r"https?://[^)\s]+", README.read_text()))
    urls = sorted(urls)
    failures: list[tuple[str, str]] = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(probe, url, args.timeout): url for url in urls}
        for future in as_completed(futures):
            url, result = future.result()
            if result.startswith(("HTTP", "ERROR")):
                failures.append((url, result))

    print(f"Checked {len(urls)} unique links; {len(failures)} unresolved")
    for url, result in sorted(failures):
        print(f"- {result}: {url}")
    return 1 if args.strict and failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

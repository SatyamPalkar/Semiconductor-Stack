"""One bounded GET per catalog URL. Link status is not content or financial validation."""

import argparse
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from pathlib import Path
from threading import Lock
from urllib.parse import urlsplit

import httpx

from semiconductor_research.sources.directory import Directory

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "data/interim/directory-links.json")
    parser.add_argument(
        "--only-new",
        action="store_true",
        help="Preserve prior observations; check only newly listed URLs",
    )
    args = parser.parse_args()
    catalog = Directory.model_validate_json(
        (ROOT / "data/catalog/semiconductor-directory.json").read_text()
    ).model_dump(mode="json")
    urls = sorted(
        {u for c in catalog["companies"] for u in [c["website"], c["investor_url"]] if u}
        | {r["url"] for r in catalog["resources"]}
    )
    previous = (
        json.loads(args.output.read_text())["results"]
        if args.only_new and args.output.exists()
        else []
    )
    retained = [r for r in previous if r["url"] in urls]
    seen = {r["url"] for r in retained}
    urls = [u for u in urls if u not in seen]
    locks = {urlsplit(u).hostname: Lock() for u in urls}

    def check(url):
        host = urlsplit(url).hostname
        result = {"url": url, "checked_at": datetime.now(UTC).isoformat(), "status": None}
        if host == "sec.gov" or host.endswith(".sec.gov") or host == "investor.tsmc.com":
            return {
                **result,
                "state": "not_requested",
                "note": "Automated fetch deliberately skipped: SEC contact identity / earlier TSMC access restriction.",
            }
        with locks[host]:
            try:
                with httpx.Client(timeout=12, follow_redirects=False) as client:
                    with client.stream(
                        "GET",
                        url,
                        headers={"User-Agent": "Semiscope/0.1 (public directory link check)"},
                    ) as response:
                        result["status"] = response.status_code
                        content = bytearray()
                        for block in response.iter_bytes():
                            content.extend(block)
                            if len(content) >= 262144:
                                break
                        match = re.search(
                            r"<title[^>]*>(.*?)</title>",
                            content.decode("utf-8", errors="replace"),
                            re.I | re.S,
                        )
                        if match:
                            result["page_title"] = re.sub(r"\s+", " ", match.group(1)).strip()[:200]
                        result["state"] = (
                            "responded"
                            if 200 <= response.status_code < 300
                            else "redirect"
                            if 300 <= response.status_code < 400
                            else "restricted"
                            if response.status_code in {401, 403, 429}
                            else "not_found"
                            if response.status_code in {404, 410}
                            else "error"
                        )
            except httpx.HTTPError as exc:
                result.update(state="error", note=type(exc).__name__)
        return result

    results = retained
    with ThreadPoolExecutor(max_workers=6) as pool:
        jobs = [pool.submit(check, url) for url in urls]
        for future in as_completed(jobs):
            results.append(future.result())
            if len(results) % 25 == 0:
                print(f"Checked {len(results)}/{len(urls)} fixed public URLs", flush=True)
    report = {
        "executed_at": datetime.now(UTC).isoformat(),
        "method": "One bounded GET per fixed catalog URL, 12s timeout, 256KiB read limit, no redirects, retries or access-control bypass. HTTP response is not content validation.",
        "results": sorted(results, key=lambda x: x["url"]),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(
        json.dumps(
            {
                state: sum(r["state"] == state for r in results)
                for state in sorted({r["state"] for r in results})
            }
        )
    )


if __name__ == "__main__":
    main()

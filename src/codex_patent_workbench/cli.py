from __future__ import annotations

import argparse
import json
from pathlib import Path

from .dedup import filter_candidates
from .inventory import build_inventory_index, load_inventory_index


def cmd_build_index(_: argparse.Namespace) -> int:
    payload = build_inventory_index()
    print(json.dumps(payload["stats"], ensure_ascii=False, indent=2))
    return 0


def cmd_summary(_: argparse.Namespace) -> int:
    payload = load_inventory_index()
    print(json.dumps(payload["stats"], ensure_ascii=False, indent=2))
    return 0


def cmd_filter_candidates(args: argparse.Namespace) -> int:
    payload = filter_candidates(Path(args.input))
    print(json.dumps({"stats": payload["stats"], "output_file": payload["output_file"]}, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Codex patent workbench CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_index = subparsers.add_parser("build-index", help="Scan existing patent library and build index.")
    build_index.set_defaults(func=cmd_build_index)

    summary = subparsers.add_parser("summary", help="Show existing inventory summary.")
    summary.set_defaults(func=cmd_summary)

    filter_parser = subparsers.add_parser("filter-candidates", help="Filter patent candidates with dedup enabled.")
    filter_parser.add_argument("--input", required=True, help="Path to candidate patent JSON list.")
    filter_parser.set_defaults(func=cmd_filter_candidates)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

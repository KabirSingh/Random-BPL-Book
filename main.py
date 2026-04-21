#!/usr/bin/env python3
"""
Pick a truly random book from the Boston Public Library system.

Picks a random catalog ID from the BPL's ID space (no seed words, no query
bias — every item in the collection has an equal shot). Displays title,
author, description, and exactly which branches have it on the shelf.

Usage:
    python3 main.py

Requires:
    pip install requests
"""

import sys

try:
    import requests
except ImportError:
    print("Missing dependency. Install with: pip install requests")
    sys.exit(1)

from bpl_api import BPL_RECORD
from bpl_connector import pick_random_book


def wrap(text: str, width: int = 58, indent: str = "  ") -> list[str]:
    words, line, lines = text.split(), indent, []
    for w in words:
        if len(line) + len(w) + (1 if line.strip() else 0) > width:
            lines.append(line)
            line = indent + w
        else:
            line += (" " if line.strip() else "") + w
    if line.strip():
        lines.append(line)
    return lines


def display(bib_id: str, info: dict, avail_data: dict) -> None:
    title    = info.get("title") or "Unknown title"
    subtitle = info.get("subtitle") or ""
    authors  = info.get("authors") or []
    fmt      = info.get("format") or ""
    year     = info.get("publicationDate") or ""
    desc     = info.get("description") or ""
    edition  = info.get("edition") or ""
    call_num = info.get("callNumber") or ""

    author_str = ", ".join(authors) if authors else "Unknown author"
    full_title = title + (f": {subtitle}" if subtitle else "")

    avail_entity  = avail_data.get("entities", {}).get("availabilities", {}).get(bib_id, {})
    total_copies  = avail_entity.get("totalCopies", "?")
    avail_copies  = avail_entity.get("availableCopies", "?")

    W   = 62
    bar = "=" * W

    print()
    print(bar)
    for line in wrap(full_title, W - 4):
        print(line)
    print(f"  by {author_str}")
    print(bar)
    if fmt:
        print(f"  Format  : {fmt}")
    if year:
        print(f"  Year    : {year}")
    if edition:
        print(f"  Edition : {edition}")
    if call_num:
        print(f"  Call #  : {call_num}")
    print(f"  Copies  : {avail_copies} available / {total_copies} in system")
    if desc:
        print()
        lines = wrap(desc, W - 4)
        for line in lines[:8]:
            print(line)
        if len(lines) > 8:
            print("  …")
    print()
    print(f"  {BPL_RECORD}/{bib_id}")
    print(bar)

    items = avail_data.get("entities", {}).get("bibItems", {})
    if not items:
        return

    branches: dict[str, list[str]] = {}
    for item in items.values():
        name   = item.get("branchName") or item.get("branch", {}).get("name") or "Unknown"
        status = item.get("availability", {}).get("status") or "UNKNOWN"
        branches.setdefault(name, []).append(status)

    on_shelf = {
        name: sum(1 for s in ss if s == "AVAILABLE")
        for name, ss in branches.items()
        if any(s == "AVAILABLE" for s in ss)
    }

    if on_shelf:
        print(f"\n  On the shelf right now:")
        for name in sorted(on_shelf):
            n = on_shelf[name]
            print(f"    {name}  —  {n} cop{'y' if n == 1 else 'ies'}")
    else:
        print("\n  No copies on shelf right now (checked out / in transit).")
        print("  Branches that own this title:")
        for name in sorted(branches):
            n = len(branches[name])
            print(f"    {name}  —  {n} cop{'y' if n == 1 else 'ies'}")
        print()
        print("  Place a hold at the link above.")

    print(bar)


def main() -> None:
    print("Picking a random book from the Boston Public Library…")
    try:
        bib_id, info, avail_data = pick_random_book()
        display(bib_id, info, avail_data)
    except (RuntimeError, requests.RequestException) as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

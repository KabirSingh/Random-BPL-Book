#!/usr/bin/env python3
"""
Pick a truly random book from a public library catalog.

Usage:
    python3 main.py                     # defaults to Detroit Public Library
    python3 main.py -l bpl              # Boston Public Library
    python3 main.py -l sfpl             # San Francisco Public Library
    python3 main.py --list              # show all supported libraries
    python3 main.py --help              # show this help message

Requires:
    pip install requests
"""

import argparse
import sys

try:
    import requests
except ImportError:
    print("Missing dependency. Install with: pip install requests")
    sys.exit(1)

from lib.connector import Book, pick_random_book
from lib.libraries import LIBRARIES


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


def display(book: Book) -> None:
    W   = 62
    bar = "=" * W

    print()
    print(bar)
    for line in wrap(book.title, W - 4):
        print(line)
    if book.authors:
        print(f"  by {', '.join(book.authors)}")
    print(bar)
    if book.format:
        print(f"  Format  : {book.format}")
    if book.year:
        print(f"  Year    : {book.year}")
    if book.edition:
        print(f"  Edition : {book.edition}")
    if book.call_number:
        print(f"  Call #  : {book.call_number}")
    print(f"  Copies  : {book.available_copies} available / {book.total_copies} in system")

    if book.description:
        print()
        lines = wrap(book.description, W - 4)
        for line in lines[:8]:
            print(line)
        if len(lines) > 8:
            print("  …")

    print()
    print(f"  {book.record_url}")
    print(bar)

    if not book.branches:
        return

    on_shelf = {
        name: v["available"]
        for name, v in book.branches.items()
        if v["available"] > 0
    }

    if on_shelf:
        print(f"\n  On the shelf right now:")
        for name in sorted(on_shelf):
            n = on_shelf[name]
            print(f"    {name}  —  {n} cop{'y' if n == 1 else 'ies'}")
    else:
        print("\n  No copies on shelf right now (checked out / in transit).")
        print("  Branches that own this title:")
        for name in sorted(book.branches):
            n = book.branches[name]["total"]
            print(f"    {name}  —  {n} cop{'y' if n == 1 else 'ies'}")
        print()
        print("  Place a hold at the link above.")

    print(bar)


def list_libraries() -> None:
    print("\nSupported libraries:\n")
    for key, lib in LIBRARIES.items():
        print(f"  {key:<12}  {lib['name']}")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="main.py",
        description=(
            "Pick a truly random book from a public library catalog.\n"
            "Every item in the collection has an equal shot — no search bias."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            "  python3 main.py                 pick a random book from Detroit Public Library\n"
            "  python3 main.py -l bpl          pick from Boston Public Library\n"
            "  python3 main.py -l sfpl         pick from San Francisco Public Library\n"
            "  python3 main.py --list          show all supported libraries\n"
        ),
    )
    parser.add_argument(
        "--library", "-l",
        default="dpl",
        metavar="ID",
        help="library ID to pick from (default: dpl). Use --list to see all options.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="list all supported libraries and exit",
    )
    args = parser.parse_args()

    if args.list:
        list_libraries()
        return

    lib_id = args.library.lower()
    if lib_id not in LIBRARIES:
        print(f"Unknown library '{lib_id}'. Run with --list to see all options, or --help for usage.")
        sys.exit(1)

    library = {"id": lib_id, **LIBRARIES[lib_id]}
    print(f"Picking a random book from the {library['name']}…")

    try:
        book = pick_random_book(library)
        display(book)
    except (RuntimeError, requests.RequestException) as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

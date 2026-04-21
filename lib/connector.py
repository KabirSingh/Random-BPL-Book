"""
Connector — orchestrates between the entry point and the DAL.
Dispatches to the right DAL based on library type and handles retry logic.
"""

import random
from dataclasses import dataclass, field

from . import bc_api
from . import dpl_api

ID_MIN = 100


@dataclass
class Book:
    library_name:    str
    title:           str
    authors:         list[str]
    format:          str
    year:            str
    edition:         str
    call_number:     str
    description:     str
    total_copies:    int | str
    available_copies: int | str
    branches:        dict  # {name: {"available": int, "total": int}}
    record_url:      str


def pick_random_book(library: dict) -> Book:
    """Pick a random valid book from any supported library."""
    if library["type"] == "bc":
        return _pick_bc(library)
    if library["type"] == "sirsi":
        return _pick_sirsi(library)
    raise ValueError(f"Unknown library type: {library['type']}")


def _pick_bc(library: dict) -> Book:
    lib_id = library["id"]
    prefix = library["bib_prefix"]
    id_max = library["id_max"]

    for _ in range(30):
        n      = random.randint(ID_MIN, id_max)
        bib_id = f"{prefix}{n}"
        avail  = bc_api.fetch_availability(lib_id, bib_id)
        if avail is None:
            continue
        info = bc_api.fetch_metadata(lib_id, bib_id)
        if info is None:
            continue

        avail_entity     = avail.get("entities", {}).get("availabilities", {}).get(bib_id, {})
        items            = avail.get("entities", {}).get("bibItems", {})
        branches: dict   = {}

        for item in items.values():
            name      = item.get("branchName") or item.get("branch", {}).get("name") or "Unknown"
            available = item.get("availability", {}).get("status") == "AVAILABLE"
            if name not in branches:
                branches[name] = {"available": 0, "total": 0}
            branches[name]["total"] += 1
            if available:
                branches[name]["available"] += 1

        return Book(
            library_name    = library["name"],
            title           = info.get("title") or "Unknown title",
            authors         = info.get("authors") or [],
            format          = info.get("format") or "",
            year            = info.get("publicationDate") or "",
            edition         = info.get("edition") or "",
            call_number     = info.get("callNumber") or "",
            description     = info.get("description") or "",
            total_copies    = avail_entity.get("totalCopies", "?"),
            available_copies= avail_entity.get("availableCopies", "?"),
            branches        = branches,
            record_url      = f"{library['record_base']}/{bib_id}",
        )

    raise RuntimeError("Could not find a valid book after 30 attempts.")


def _pick_sirsi(library: dict) -> Book:
    id_min = library.get("id_min", ID_MIN)
    id_max = library["id_max"]

    for _ in range(30):
        title_id = random.randint(id_min, id_max)
        avail    = dpl_api.fetch_availability(title_id)
        if avail is None:
            continue
        title = dpl_api.fetch_title(title_id)
        if not title:
            continue

        return Book(
            library_name     = library["name"],
            title            = title,
            authors          = [],
            format           = "",
            year             = "",
            edition          = "",
            call_number      = avail["call_number"],
            description      = "",
            total_copies     = avail["total_copies"],
            available_copies = avail["available_copies"],
            branches         = avail["branches"],
            record_url       = dpl_api.record_url(title_id),
        )

    raise RuntimeError("Could not find a valid book after 30 attempts.")

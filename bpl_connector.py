"""
Connector — orchestrates between the entry point and the DAL.
Handles retry logic and ID generation so neither layer needs to know about it.
"""

import random

from bpl_api import ID_MIN, ID_MAX, fetch_availability, fetch_metadata


def make_bib_id(n: int) -> str:
    return f"S75C{n}"


def pick_random_book() -> tuple[str, dict, dict]:
    """
    Pick a random valid bib ID and return (bib_id, briefInfo, availability_data).
    Retries silently on 404s (gaps in the ID space).
    """
    for _ in range(30):
        n      = random.randint(ID_MIN, ID_MAX)
        bib_id = make_bib_id(n)
        avail  = fetch_availability(bib_id)
        if avail is None:
            continue  # gap in the ID space — try another
        info = fetch_metadata(bib_id)
        if info is None:
            continue
        return bib_id, info, avail

    raise RuntimeError("Could not find a valid book after 30 attempts.")

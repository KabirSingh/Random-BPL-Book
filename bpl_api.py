"""
Data Access Layer — all network calls to the BPL / Bibliocommons API.
"""

import requests

GATEWAY    = "https://gateway.bibliocommons.com/v2/libraries/bpl"
BPL_RECORD = "https://bpl.bibliocommons.com/v2/record"

# BPL bib IDs follow the pattern S75C{number}.
# Valid IDs were found up to ~9,560,000; ~55% of random integers in this
# range correspond to real catalog records.
ID_MIN = 100
ID_MAX = 9_560_000


def fetch_availability(bib_id: str) -> dict | None:
    """Returns the availability JSON, or None if the ID doesn't exist."""
    r = requests.get(f"{GATEWAY}/bibs/{bib_id}/availability", timeout=15)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return r.json()


def fetch_metadata(bib_id: str) -> dict | None:
    """Returns the briefInfo dict for a bib ID, or None on failure."""
    r = requests.get(f"{GATEWAY}/bibs", params={"metadataIds": bib_id, "locale": "en-US"}, timeout=15)
    if not r.ok:
        return None
    bibs = r.json().get("entities", {}).get("bibs", {})
    bib  = bibs.get(bib_id)
    return bib.get("briefInfo") if bib else None

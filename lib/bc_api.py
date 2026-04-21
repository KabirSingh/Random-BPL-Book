"""
Data Access Layer — BiblioCommons API.
Works with any library on the BiblioCommons platform.
"""

import requests

_GATEWAY = "https://gateway.bibliocommons.com/v2/libraries"


def fetch_availability(library_id: str, bib_id: str) -> dict | None:
    """Returns the availability JSON, or None if the ID doesn't exist."""
    r = requests.get(f"{_GATEWAY}/{library_id}/bibs/{bib_id}/availability", timeout=15)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return r.json()


def fetch_metadata(library_id: str, bib_id: str) -> dict | None:
    """Returns the briefInfo dict for a bib ID, or None on failure."""
    r = requests.get(
        f"{_GATEWAY}/{library_id}/bibs",
        params={"metadataIds": bib_id, "locale": "en-US"},
        timeout=15,
    )
    if not r.ok:
        return None
    bibs = r.json().get("entities", {}).get("bibs", {})
    bib  = bibs.get(bib_id)
    return bib.get("briefInfo") if bib else None

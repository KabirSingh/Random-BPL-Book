"""
Data Access Layer — Detroit Public Library (SirsiDynix).
"""

import re
import xml.etree.ElementTree as ET

import requests

_SIRSI_API   = "https://sdws02.sirsidynix.net/detp_ilsws/rest/standard/lookupTitleInfo"
_CATALOG_URL = "https://detp.ent.sirsi.net/client/en_US/default/search/detailnonmodal"
_NS          = "http://schemas.sirsidynix.com/symws/standard"

_UNAVAILABLE = {"CHECKEDOUT", "TRANSIT", "INTRANSIT", "MISSING", "LOST", "BINDERY", "ILL"}

BRANCH_NAMES = {
    "BREL": "Elmwood Park Branch",
    "BRRD": "Redford Branch",
}


def _t(tag: str) -> str:
    return f"{{{_NS}}}{tag}"


def fetch_availability(title_id: int) -> dict | None:
    """
    Returns a normalised availability dict or None if the record doesn't exist
    or has no physical book items.

    Return shape:
        {
            "call_number":       str,
            "total_copies":      int,
            "available_copies":  int,
            "branches": {
                branch_name: {"available": int, "total": int},
                ...
            },
        }
    """
    r = requests.get(
        _SIRSI_API,
        params={"clientID": "DS_CLIENT", "titleID": title_id, "includeItemInfo": "true"},
        timeout=15,
    )
    if not r.ok:
        return None

    try:
        root = ET.fromstring(r.text)
    except ET.ParseError:
        return None

    title_info = root.find(_t("TitleInfo"))
    if title_info is None:
        return None

    branches:        dict[str, dict] = {}
    total_copies     = 0
    available_copies = 0
    call_number      = ""

    for call_info in title_info.findall(_t("CallInfo")):
        code        = call_info.findtext(_t("libraryID")) or ""
        branch_name = BRANCH_NAMES.get(code, code)
        if not call_number:
            call_number = call_info.findtext(_t("callNumber")) or ""

        for item in call_info.findall(_t("ItemInfo")):
            item_type = (item.findtext(_t("itemTypeID")) or "").upper()
            if "BOOK" not in item_type:
                continue

            loc       = (item.findtext(_t("currentLocationID")) or "").upper()
            available = loc not in _UNAVAILABLE

            total_copies += 1
            if available:
                available_copies += 1

            if branch_name not in branches:
                branches[branch_name] = {"available": 0, "total": 0}
            branches[branch_name]["total"] += 1
            if available:
                branches[branch_name]["available"] += 1

    if total_copies == 0:
        return None  # no physical book items

    return {
        "call_number":      call_number,
        "total_copies":     total_copies,
        "available_copies": available_copies,
        "branches":         branches,
    }


def fetch_title(title_id: int) -> str | None:
    """Returns the book title from the catalog page <title> tag, or None."""
    url = f"{_CATALOG_URL}/ent:$002f$002fSD_ILS$002f0$002fSD_ILS:{title_id}/one"
    r   = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
    if not r.ok:
        return None
    match = re.search(r"<title[^>]*>([^<]+)</title>", r.text, re.IGNORECASE)
    return match.group(1).strip() if match else None


def record_url(title_id: int) -> str:
    return f"{_CATALOG_URL}/ent:$002f$002fSD_ILS$002f0$002fSD_ILS:{title_id}/one"

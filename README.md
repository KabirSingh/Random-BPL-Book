# Random Library Book

Pick a completely random book from a public library catalog and find out exactly where to get it.

No seed words, no search bias — the app picks a random catalog ID directly from the library's ID space, so every item in the collection has an equal shot.

## Web app

https://kabirsingh.github.io/Random-BPL-Book/

Supported libraries:

| Library | Catalog system | Author/description |
|---|---|---|
| Boston Public Library | BiblioCommons | ✓ |
| Detroit Public Library | SirsiDynix | — |
| San Francisco Public Library | BiblioCommons | ✓ |
| Chicago Public Library | BiblioCommons | ✓ |
| Seattle Public Library | BiblioCommons | ✓ |
| Toronto Public Library | BiblioCommons | ✓ |

> Detroit Public Library uses SirsiDynix, which doesn't expose a public API for bibliographic data. DPL results show title, call number, and branch availability — click the record link for full details.

## CLI (Boston Public Library only)

```
Picking a random book from the Boston Public Library…

==============================================================
  Frog
  by Taylor, Kim
==============================================================
  Format  : BK
  Year    : 1991
  Edition : 1st American ed
  Call #  : QL668.E2 T24 1991
  Copies  : 2 available / 2 in system

  Photographs and text show the development of a frog from
  the egg stage through its first year.

  https://bpl.bibliocommons.com/v2/record/S75C698960
==============================================================

  On the shelf right now:
    BPL-High Density Offsite Storage  —  1 copy
    BPS- Quincy Elementary School  —  1 copy
==============================================================
```

### Requirements

Python 3.10+ and the `requests` library:

```bash
pip install requests
```

### Usage

```bash
python3 main.py
```

## How it works

### BiblioCommons libraries

BiblioCommons powers the catalog for Boston, San Francisco, Chicago, Seattle, Toronto, and many other public libraries. Every physical item has an ID of the form `S{N}C{number}` where `N` is the library's BiblioCommons ID. The app picks a random integer in the known valid range, checks whether a record exists, and fetches title, author, description, and per-branch availability via BiblioCommons' public API. The hit rate is ~55%, so it typically resolves in 1–2 tries.

### Detroit Public Library

DPL uses SirsiDynix. The app calls SirsiDynix's `lookupTitleInfo` REST endpoint to get branch availability, and fetches the catalog page title for the book name. Author and description aren't available through the public API.

### Architecture

```
main.py           — CLI entry point
bpl_connector.py  — orchestration layer
bpl_api.py        — data access layer (BiblioCommons API)
docs/index.html   — web frontend (GitHub Pages)
worker.js         — Cloudflare Worker CORS proxy
```

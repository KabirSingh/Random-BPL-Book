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

## CLI

Supports all the same libraries as the web app. Defaults to Detroit Public Library.

### Requirements

Python 3.10+ and the `requests` library:

```bash
pip install requests
```

### Usage

```bash
python3 main.py                  # Detroit Public Library (default)
python3 main.py -l bpl           # Boston Public Library
python3 main.py -l sfpl          # San Francisco Public Library
python3 main.py -l chipublib     # Chicago Public Library
python3 main.py -l seattle       # Seattle Public Library
python3 main.py -l tpl           # Toronto Public Library
python3 main.py --list           # show all supported libraries
python3 main.py --help           # show usage
```

## How it works

### BiblioCommons libraries

BiblioCommons powers the catalog for Boston, San Francisco, Chicago, Seattle, Toronto, and many other public libraries. Every physical item has an ID of the form `S{N}C{number}` where `N` is the library's BiblioCommons ID. The app picks a random integer in the known valid range, checks whether a record exists, and fetches title, author, description, and per-branch availability via BiblioCommons' public API. The hit rate is ~55%, so it typically resolves in 1–2 tries.

### Detroit Public Library

DPL uses SirsiDynix. The app calls SirsiDynix's `lookupTitleInfo` REST endpoint to get branch availability, and fetches the catalog page title for the book name. Author and description aren't available through the public API.

### Architecture

```
main.py                — CLI entry point
lib/libraries.py       — library registry and config
lib/connector.py       — orchestration layer
lib/bc_api.py          — DAL for BiblioCommons libraries
lib/dpl_api.py         — DAL for Detroit Public Library (SirsiDynix)
docs/index.html        — web frontend (GitHub Pages)
worker.js              — Cloudflare Worker CORS proxy
```

# Random BPL Book

Pick a completely random book from the Boston Public Library system and find out exactly where to get it.

No seed words, no search bias — the script picks a random catalog ID directly from BPL's ID space, so every item in the collection has an equal shot.

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

## How it works

BPL uses [BiblioCommons](https://www.bibliocommons.com/) for its catalog. Every physical item has an ID of the form `S75C{number}` (75 is BPL's library ID). The script picks a random integer in the known valid range, checks whether a catalog record exists at that ID, and if so fetches the title, author, description, and per-branch availability — all via BiblioCommons' public API. The hit rate is ~55%, so it typically resolves in 1–2 tries.

## Requirements

Python 3.10+ and the `requests` library:

```bash
pip install requests
```

## Usage

```bash
python3 random_bpl_book.py
```

Run it whenever you want a random book. If all copies are checked out, the output includes a direct link to place a hold.

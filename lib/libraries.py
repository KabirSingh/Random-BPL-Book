"""
Registry of supported libraries and their configuration.
"""

LIBRARIES: dict[str, dict] = {
    # ── BiblioCommons ──────────────────────────────────────────────────────────
    "bpl": {
        "name":        "Boston Public Library",
        "type":        "bc",
        "bib_prefix":  "S75C",
        "id_max":      9_560_000,
        "record_base": "https://bpl.bibliocommons.com/v2/record",
    },
    "sfpl": {
        "name":        "San Francisco Public Library",
        "type":        "bc",
        "bib_prefix":  "S93C",
        "id_max":      6_200_000,
        "record_base": "https://sfpl.bibliocommons.com/v2/record",
    },
    "chipublib": {
        "name":        "Chicago Public Library",
        "type":        "bc",
        "bib_prefix":  "S126C",
        "id_max":      2_700_000,
        "record_base": "https://chipublib.bibliocommons.com/v2/record",
    },
    "seattle": {
        "name":        "Seattle Public Library",
        "type":        "bc",
        "bib_prefix":  "S30C",
        "id_max":      1_500_000,
        "record_base": "https://seattle.bibliocommons.com/v2/record",
    },
    "tpl": {
        "name":        "Toronto Public Library",
        "type":        "bc",
        "bib_prefix":  "S234C",
        "id_max":      3_800_000,
        "record_base": "https://tpl.bibliocommons.com/v2/record",
    },
    # ── SirsiDynix ────────────────────────────────────────────────────────────
    "dpl": {
        "name":    "Detroit Public Library",
        "type":    "sirsi",
        "id_min":  10_000,
        "id_max":  1_500_000,
    },
}

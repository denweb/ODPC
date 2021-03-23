from statistics import mean
from urllib.parse import urlparse


def check_metadata(metadaten):
    res = {
        "titel": 0,
        "beschreibung": 0,
        "tags": 0,
        "geo": 0
    }

    if metadaten["titel"] and metadaten["titel"] != "None":
        res["titel"] += 4
    if metadaten["beschreibung"] and metadaten["beschreibung"] != "None":
        res["beschreibung"] += 3
    if metadaten["tags"] and metadaten["tags"] != "[]":
        res["tags"] += 1
    if metadaten["geo"] and metadaten["geo"] != "None":
        res["geo"] += 1

    return res


def check_valid_metadata(metadaten, kontakte):
    res = 0

    # check einzelne felder.
    for kontakt in [metadaten["autor"], metadaten["verwalter"]]:
        if kontakt in kontakte["beide"]:
            res += 1
        elif kontakt in kontakte["name"] or kontakt in kontakte["email"]:
            res += 0.5

    url_parse = urlparse(metadaten["url"])
    if all([url_parse.scheme, url_parse.netloc]):
        res += 1

    res = res/5
    return res


def get_genau(meta, kontakte):
    res = {
        "titel": 0,
        "beschreibung": 0,
        "tags": 0,
        "geo": 0,
        "syntax": 0
    }

    meta_inf = [check_metadata(metadaten) for metadaten in meta]
    for feld in ["titel", "beschreibung", "tags", "geo"]:
        res[feld] = mean([res[feld] for res in meta_inf])

    res["syntax"] = mean([check_valid_metadata(metadaten, kontakte) for metadaten in meta])

    print(res)

    return res

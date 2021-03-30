from statistics import mean
from urllib.parse import urlparse
from framework.utility.scores import calc_score


def check_metadata(metadaten):
    res = {
        "titel": 0,
        "beschreibung": 0,
        "tags": 0,
        "geodaten": 0
    }

    if metadaten["titel"] and metadaten["titel"] != "None":
        res["titel"] += 4
    if metadaten["beschreibung"] and metadaten["beschreibung"] != "None":
        res["beschreibung"] += 3
    if metadaten["tags"] and metadaten["tags"] != "[]":
        res["tags"] += 1
    if metadaten["geo"] and metadaten["geo"] != "None":
        res["geodaten"] += 1

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


# Todo: Weitere Felder auf Existenz / Validität prüfen.
# Todo: Informationsgehalt? Lesbarkeit?
def get_genau(meta, kontakte, portal):
    res = {
        "titel": 0,
        "beschreibung": 0,
        "tags": 0,
        "geodaten": 0,
        "metaValidität": 0
    }

    meta_inf = [check_metadata(metadaten) for metadaten in meta]
    for feld in ["titel", "beschreibung", "tags", "geodaten"]:
        res[feld] = mean([res[feld] for res in meta_inf])

    res["metaValidität"] = mean([check_valid_metadata(metadaten, kontakte) for metadaten in meta])

    res["score"] = calc_score(res)
    res["gewScore"] = res["score"]

    res["portalID"] = portal

    return res

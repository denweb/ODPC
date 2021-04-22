from statistics import mean
from urllib.parse import urlparse
from framework.utility.scores import calc_score


def check_metadata(metadaten):
    """
    Überprüft das Vorhandensein von Titel, Beschreibung, Tags und Geodaten in den Metadaten.
    """
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
    """
    Überprüft, ob die angegebenen Metadaten eines Datensatzes syntaktisch valide sind.
    """
    res = 0

    # check einzelne felder für Kontakte
    for kontakt in [metadaten["autor"], metadaten["verwalter"]]:
        if kontakt in kontakte["beide"]:
            res += 1
        elif kontakt in kontakte["name"] or kontakt in kontakte["email"]:
            res += 0.5

    # check URL
    url_parse = urlparse(metadaten["url"])
    if all([url_parse.scheme, url_parse.netloc]):
        res += 1

    res = res/3
    return res


# Todo: Weitere Felder auf Existenz / Validität prüfen.
# Todo: Informationsgehalt? Lesbarkeit?
def get_genau(meta, kontakte, portal):
    """
    Berechnet die Werte der Metriken in der Dimension Genauigkeit.
    :param meta: Metadaten eines OGD-Portals
    :param kontakte: IDs von validen Kontakten in der DB
    :param portal: Portal-ID
    :return: Die bestimmten Metrik-Werte der Dimension in einem Dictionary
    """
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

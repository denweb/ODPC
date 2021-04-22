from statistics import mean
from ast import literal_eval
from framework.utility.scores import calc_score


def get_gew_vollst(metadaten):
    """
    überprüft ob in den Metadaten eines Datensatzes Angaben zu Titel, Beschreibung, Autor, Verwalter,
    Geo-Bezug, Organisation, Erstelldatum, Updatedatum, zugeordneten Gruppen, Tags,
    und einer Lizenz gemacht sind.
    """
    res = 0

    if metadaten["titel"] and metadaten["titel"] != "None":
        res += 5
    if metadaten["beschreibung"] and metadaten["beschreibung"] != "None":
        res += 4
    if metadaten["autor"]:
        res += 1
    if metadaten["verwalter"]:
        res += 1
    if metadaten["geo"] and metadaten["geo"] != "None":
        res += 1
    if metadaten["organisation"] and metadaten["organisation"] != 1:
        res += 1
    if metadaten["erstellDatum"] and metadaten["erstellDatum"] != 4:
        res += 1
    if metadaten["updateDatum"] and metadaten["updateDatum"] != 4:
        res += 1
    if metadaten["gruppe"] and metadaten["gruppe"] != "[]":
        res += 1
    if metadaten["tags"] and metadaten["tags"] != "[]":
        res += 3
    if metadaten["lizenz"] and metadaten["lizenz"] not in [7, 11, 18, 31, 45]:
        res += 1

    return res


def get_roh_fehler(roh, vollst_fehler):

    res = {
        "rohZelle": 0,
        "rohReihe": 0,
        "rohLabel": 0
    }

    zelle = []
    reihe = []
    label = []

    for data in roh:
        if all([data["fehler"] is not None, data["fehler"] != "None"]):
            fehler = set(literal_eval(data["fehler"]))

            # Zelle
            if not fehler.intersection(vollst_fehler["zelle"]):
                zelle.append(1)
            else:
                zelle.append(0)

            # Reihe
            if not fehler.intersection(vollst_fehler["reihe"]):
                reihe.append(1)
            else:
                reihe.append(0)

            # Label
            if not fehler.intersection(vollst_fehler["label"]):
                label.append(1)
            else:
                label.append(0)

    if zelle:
        res["rohZelle"] = mean(zelle)
    if reihe:
        res["rohReihe"] = mean(reihe)
    if label:
        res["rohLabel"] = mean(label)

    return res


def get_vollst(meta, roh, vollst_fehler, portal):
    """
    Berechnet die Werte der Metriken in der Dimension Vollständigkeit.
    :param meta: Metadaten eines OGD-Portals
    :param roh: Rohdateninformationen eines OGD-Portals
    :param vollst_fehler: IDs von Fehlern, die die Vollständigkeit betreffen, in der DB
    :param portal: Portal-ID
    :return: Die bestimmten Metrik-Werte der Dimension in einem Dictionary
    """
    res = {
        "gewVollst": mean([get_gew_vollst(metadaten) for metadaten in meta]) * 7 / 20,
        "rohZelle": 0,
        "rohReihe": 0,
        "rohLabel": 0
    }

    fehler_metr = get_roh_fehler(roh, vollst_fehler)

    for metr in fehler_metr:
        res[metr] = fehler_metr[metr]

    res["score"] = calc_score(res)
    res["gewScore"] = res["score"]

    res["portalID"] = portal

    return res

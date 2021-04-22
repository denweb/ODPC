from statistics import mean
from framework.utility.scores import calc_score


def get_neue_daten(akt_daten, datum_ids):
    """
    Überprüft, ob Daten aus den Jahren '20 und '21 im Datensatz vorhanden sind.
    """
    res = 0
    if akt_daten.intersection(datum_ids):
        res = 2

    return res


def get_alte_daten(akt_daten, meta_datum):
    """
    Überprüft, ob ein Datensatz aus dem Jahr '20 oder '21 stammt.
    """
    res = 0
    if meta_datum in akt_daten:
        res = 2

    return res


def get_akt(metadaten, akt_daten, datum_ids, portal):
    """
    Berechnet die Werte der Metriken in der Dimension Aktualität.
    :param metadaten: Metadateninformationen eines OGD-Portals
    :param akt_daten: Die IDs der Daten aus den Jahren '20 und '21 in der DB
    :param datum_ids: Die IDs der Daten des zu untersuchenden OGD-Portals in der DB.
    :param portal: Portal-ID
    :return: Die bestimmten Metrik-Werte der Dimension in einem Dictionary
    """
    res = {
        "updates": mean([3 if meta["updateDatum"] != 3 else 0 for meta in metadaten]),
        "erstellt": mean([3 if meta["erstellDatum"] != 3 else 0 for meta in metadaten]),
        "neueDaten": get_neue_daten(akt_daten, datum_ids),
        "alterDaten": mean([get_alte_daten(akt_daten, meta["erstellDatum"]) for meta in metadaten])
    }

    res["score"] = calc_score(res)
    res["gewScore"] = res["score"]*0.7

    res["portalID"] = portal

    return res

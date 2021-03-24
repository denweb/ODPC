from statistics import mean
import datetime


def get_neue_daten(akt_daten, datum_ids):

    res = 0
    if akt_daten.intersection(datum_ids):
        res = 2

    return res


def get_akt(metadaten, akt_daten, datum_ids):
    res = {
        "updates": mean([5 for meta in metadaten if meta["updateDatum"] != 4]),
        "erstellt": mean([3 for meta in metadaten if meta["erstellDatum"] != 4]),
        "neueDaten": get_neue_daten(akt_daten, datum_ids),
        "alterDaten": 0,
    }

    return res

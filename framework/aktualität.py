from statistics import mean
from framework.utility.scores import calc_score


def get_neue_daten(akt_daten, datum_ids):

    res = 0
    if akt_daten.intersection(datum_ids):
        res = 2

    return res


def get_alte_daten(akt_daten, meta_datum):
    res = 0
    if meta_datum in akt_daten:
        res = 2

    return res


def get_akt(metadaten, akt_daten, datum_ids):
    res = {
        "updates": mean([3 if meta["updateDatum"] != 4 else 0 for meta in metadaten]),
        "erstellt": mean([3 if meta["erstellDatum"] != 4 else 0 for meta in metadaten]),
        "neueDaten": get_neue_daten(akt_daten, datum_ids),
        "alterDaten": mean([get_alte_daten(akt_daten, meta["erstellDatum"]) for meta in metadaten])
    }

    res["score"] = calc_score(res)
    res["gewScore"] = res["score"]*0.7

    return res

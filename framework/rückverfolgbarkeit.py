from statistics import mean
from framework.utility.scores import calc_score


def get_rue(meta, portal):
    """
    Berechnet die Werte der Metriken in der Dimension Rückverfolgbarkeit.
    :param meta: Metadaten eines OGD-Portals
    :param portal: Portal-ID
    :return: Die bestimmten Metrik-Werte der Dimension in einem Dictionary
    """
    res = {
        "quelle": mean([10 if data["organisation"] != 1 else 0 for data in meta])
    }

    res["score"] = calc_score(res)
    res["gewScore"] = res["score"]*0.3

    res["portalID"] = portal

    return res

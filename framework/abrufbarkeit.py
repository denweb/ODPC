from statistics import mean
from framework.utility.scores import calc_score


def get_abr(rohdaten, portal_domain, portal):
    """
    Berechnet die Werte der Metriken in der Dimension Abrufbarkeit.
    :param rohdaten: Rohdateninformationen eines OGD-Portals
    :param portal_domain: Domain des OGP-Portals (String)
    :param portal: Portal-ID
    :return: Die bestimmten Metrik-Werte der Dimension in einem Dictionary
    """
    res = {
        "linkOnline": mean([9 if data["online"] == "True" else 0 for data in rohdaten]),
        "linkIntern": mean([1 if portal_domain in data["link"] else 0 for data in rohdaten]),
    }

    res["score"] = calc_score(res)
    res["gewScore"] = res["score"]

    res["portalID"] = portal

    return res

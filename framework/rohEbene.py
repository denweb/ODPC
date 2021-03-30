from framework.utility.scores import calc_score


def get_roh_metriken(portal, vollst, off, val):

    res = {
        "rohZelle": vollst["rohZelle"],
        "rohReihe": vollst["rohReihe"],
        "rohLabel": vollst["rohLabel"],
        "dfML": off["dfML"],
        "dfOffen": off["dfOffen"],
        "rdLesbar": val["rdLesbar"],
        "rdValide": val["rdValide"]
    }

    res["score"] = calc_score(res)

    res["portalID"] = portal

    return res

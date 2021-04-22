from framework.utility.scores import calc_score

# Aktuell nicht gebraucht.
def get_portal_metriken(portal, akt, div, abr):

    res = {
        "neueDaten": akt["neueDaten"],
        "durchEndp": div["durchEndp"],
        "varianceEndp": div["varianceEndp"],
        "durchDF": div["durchDF"],
        "varianceDF": div["varianceDF"],
        "durchTags": div["durchTags"],
        "varianceTags": div["varianceTags"],
        "anteilOrg": div["anteilOrg"],
        "varianceOrg": div["varianceOrg"],
    }

    res["score"] = calc_score(res)

    res["portalID"] = portal

    return res

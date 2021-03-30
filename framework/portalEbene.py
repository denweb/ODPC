from framework.utility.scores import calc_score

def get_portal_metriken(portal, akt, div, abr):

    res = {
        "neueDaten": akt["neueDaten"],
        "durchEndp": div["durchEndp"],
        "stdevEndp": div["stdevEndp"],
        "durchDF": div["durchDF"],
        "stdevDF": div["stdevDF"],
        "durchTags": div["durchTags"],
        "stdevTags": div["stdevTags"],
        "anteilOrg": div["anteilOrg"],
        "stdevOrg": div["stdevOrg"],
        "linkOnline": abr["linkOnline"]
    }

    res["score"] = calc_score(res)

    res["portalID"] = portal

    return res

from framework.utility.scores import calc_score

# Aktuell nicht gebraucht.
def get_meta_metriken(portal, genau, vollst, akt, abr, off, kon, rue):

    res = {
        "metaValidität": genau["metaValidität"],
        "geodaten": genau["geodaten"],
        "titel": genau["titel"],
        "beschreibung": genau["beschreibung"],
        "tags": genau["tags"],
        "gewVollst": vollst["gewVollst"],
        "updates": akt["updates"],
        "erstellt": akt["erstellt"],
        "alterDaten": akt["alterDaten"],
        "linkIntern": abr["linkIntern"],
        "linkOnline": abr["linkOnline"],
        "lizenzOffen": off["lizenzOffen"],
        "autorValide": kon["autorValide"],
        "verwalterValide": kon["verwalterValide"],
        "quelle": rue["quelle"]
    }

    res["score"] = calc_score(res)

    res["portalID"] = portal

    return res

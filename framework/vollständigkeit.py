from statistics import mean


def get_gew_vollst(metadaten):
    res = 0

    if metadaten["titel"] and metadaten["titel"] != "None":
        res += 5
    if metadaten["beschreibung"] and metadaten["beschreibung"] != "None":
        res += 4
    if metadaten["autor"] and metadaten["autor"] != 3:
        res += 1
    if metadaten["verwalter"] and metadaten["verwalter"] != 3:
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


#Todo: Das Rohdaten...
def get_rohdaten_vollst():
    pass


def get_vollst(meta):
    res = {
        "gewVollst": 0,
        "rohZelle": 0,
        "rohReihe": 0,
        "rohLabel": 0,
    }

    # gew. Vollständigkeit
    res["gewVollst"] = mean([get_gew_vollst(metadaten) for metadaten in meta])*7/20

    return res

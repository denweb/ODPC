from statistics import mean
from ast import literal_eval


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


# Todo: Warum gew. Vollständigkeit?
#  Nicht sinnvoller, einach vollständigkeit & gew. in Genauigkeit - wegen Informationsgehalt?
def get_vollst(meta, roh, vollst_fehler):
    res = {
        "gewVollst": mean([get_gew_vollst(metadaten) for metadaten in meta])*7/20,
        "rohZelle": mean([1 if not set(literal_eval(data["fehler"])).intersection(vollst_fehler["zelle"]) else 0
                          for data in roh
                          if data["anzahlFehler"] is not None]),
        "rohReihe": mean([1 if not set(literal_eval(data["fehler"])).intersection(vollst_fehler["reihe"]) else 0
                          for data in roh
                          if data["anzahlFehler"] is not None]),
        "rohLabel": mean([1 if not set(literal_eval(data["fehler"])).intersection(vollst_fehler["label"]) else 0
                          for data in roh
                          if data["anzahlFehler"] is not None]),
    }

    return res

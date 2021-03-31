from statistics import mean
from ast import literal_eval
from framework.utility.scores import calc_score


def get_lesbar(data, se_fehler):
    res = 0
    try:
        fehler = set(literal_eval(data["fehler"]))
    except TypeError:
        fehler = set()

    # Wenn Datei lesbar ist, sollte auch Anzahl d. Fehler gegeben sein.
    # Nur Anzahl Fehler gegeben reicht nicht, da "nicht lesbar" auch ein Fehler sein kann.
    if all([any([data["anzahlFehler"] != "None", data["anzahlFehler"] is not None]), not fehler.intersection(se_fehler)]):
        res += 5

    return res


def get_valide(data):
    res = 0

    # Anzahl, weil "valide" aktuell noch unzuverlässig mit unbestimmter Fehlerquelle. Todo für später.
    if data["anzahlFehler"] == 0:
        res += 5

    return res


def get_val(roh, se_fehler, portal):
    res = {
        "rdLesbar": 0,
        "rdValide": 0,
    }

    rdlesbar_roh = [get_lesbar(data, se_fehler) for data in roh if data["valide"] != 2]
    rdvalide_roh = [get_valide(data) for data in roh if data["valide"] != 2]

    if rdlesbar_roh:
        res["rdLesbar"] = mean(rdlesbar_roh)
    if rdvalide_roh:
        res["rdValide"] = mean(rdvalide_roh)

    res["score"] = calc_score(res)
    res["gewScore"] = res["score"]

    res["portalID"] = portal

    return res

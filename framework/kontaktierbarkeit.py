from statistics import mean
from framework.utility.scores import calc_score


def check_kontakt_valide(kontakt, val_kontakte):
    """
    Überprüft, ob syntaktisch valide Informationen zum Autor und Verwalter eines Datensatzes angegeben wurden.
    """
    res = 0

    if kontakt in val_kontakte["beide"]:
        res += 5
    elif any([kontakt in val_kontakte["name"], kontakt in val_kontakte["email"]]):
        res += 2.5

    return res


def get_kon(meta, kontakte, portal):
    """
    Berechnet die Werte der Metriken in der Dimension Kontaktierbarkeit.
    :param meta: Metadaten eines OGD-Portals
    :param kontakte: IDs von validen Kontakten in der DB
    :param portal: Portal-ID
    :return: Die bestimmten Metrik-Werte der Dimension in einem Dictionary
    """
    res = {
        "autorValide": mean([check_kontakt_valide(datensatz["autor"], kontakte) for datensatz in meta]),
        "verwalterValide": mean([check_kontakt_valide(datensatz["verwalter"], kontakte) for datensatz in meta])
    }

    res["score"] = calc_score(res)
    res["gewScore"] = res["score"]*0.3

    res["portalID"] = portal

    return res

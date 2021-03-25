from statistics import mean


def check_kontakt_valide(kontakt, val_kontakte):
    res = 0

    if kontakt in val_kontakte["beide"]:
        res += 5
    elif any([kontakt in val_kontakte["name"], kontakt in val_kontakte["email"]]):
        res += 2.5

    return res


def get_kon(meta, kontakte):
    res = {
        "autorValide": mean([check_kontakt_valide(datensatz["autor"], kontakte) for datensatz in meta]),
        "verwalterValide": mean([check_kontakt_valide(datensatz["verwalter"], kontakte) for datensatz in meta])
    }

    return res

from statistics import mean
from framework.utility.lizenzen import nicht_offen


# Todo: Nicht offene Lizenzen IDs anpassen, sobald DB final ist.
def get_off(meta, roh, dateiformate_ids):
    res = {
        "dfML": mean([4 if rohdatei["dateiTypReal"] in dateiformate_ids["dateiformate_mr"] else 0 for rohdatei in roh]),
        "dfOffen": mean([2 if rohdatei["dateiTypReal"] in dateiformate_ids["dateiformate_np"] else 0 for rohdatei in roh]),
        "lizenzOffen": mean([4 if datensatz["lizenz"] not in nicht_offen else 0 for datensatz in meta])
    }

    return res

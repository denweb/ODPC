from statistics import mean
from ast import literal_eval


def get_anteilPublisher(meta):
    pass


def get_div(meta, roh):
    res = {
        "anteilPublisher": 0,
    }

    # Publisher/organisationen auf Portal
    publisher = set(data["organisation"] for data in meta if data["organisation"] != 1)

    # Lizenzen auf Portal
    lizenzen = set(data["lizenz"] for data in meta if data["lizenz"] not in {2, 25, 13, 5})

    # Distributionen pro Datensatz
    distr_pro_ds = len(roh)/len(meta)

    # Dateiformate pro Datensatz
    df_pro_ds = []

    t = {}
    for data in roh:
        if data["metaDatensatz"] in t:
            t[data["metaDatensatz"]] += 1
        else:
            t[data["metaDatensatz"]] = 1
    anteil_df_k = [t[d] for d in t]


    return res

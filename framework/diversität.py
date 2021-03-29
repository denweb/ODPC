from statistics import mean, median, pstdev
from ast import literal_eval


def get_anteilPublisher(meta):
    # Publisher/organisationen auf Portal
    publisher = set(data["organisation"] for data in meta if data["organisation"] != 1)


def get_stdev_tags(meta):
    res = 0

    t = [tag for data in meta for tag in literal_eval(data["tags"]) if tag != 999999999]

    t_count = dict()
    for tag in t:
        t_count[tag] = t_count.get(tag, 0) + 1

    def_tags = pstdev(list(t_count.values()))

    if def_tags < 10:
        res = 1

    return res




def get_div(meta, roh):
    res = {
        "anteilDF": 0,
        "anteilEndp": 0,
        "anteilPublisher": 0,
        "devTags": get_stdev_tags(meta)
    }

    # Distributionen pro Datensatz
    distr_pro_ds = len(roh)/len(meta)

    # Dateiformate pro Datensatz
    df_pro_ds = []

    endp = {}
    form = {}
    for data in roh:
        if data["metaDatensatz"] in endp:
            endp[data["metaDatensatz"]] += 1
        else:
            endp[data["metaDatensatz"]] = 1

        if data["metaDatensatz"] in form:
            if all([data["dateiTypReal"], data["dateiTypReal"] != 1]):
                form[data["metaDatensatz"]].add(data["dateiTypReal"])
        else:
            if all([data["dateiTypReal"], data["dateiTypReal"] != 1]):
                form[data["metaDatensatz"]] = {data["dateiTypReal"]}

    endpunkte_pro_ds = [endp[d] for d in endp]

    df_pro_ds = [len(form[d]) for d in form]

    print(mean(endpunkte_pro_ds), distr_pro_ds)

    #print("mean e: {}, med e: {}, mean d: {}, med e: {}".format(mean(endpunkte_pro_ds), median(endpunkte_pro_ds), mean(df_pro_ds), median(df_pro_ds)))

    return res

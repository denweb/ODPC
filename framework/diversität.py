from statistics import mean, median, pstdev
from ast import literal_eval
from framework.utility.scores import calc_score


def get_end(roh):
    res = {
        "durchEndp": 0,
        "stdevEndp": 0
    }

    endp_counter = {}

    for data in roh:
        endp_counter[data["metaDatensatz"]] = endp_counter.get(data["metaDatensatz"], 0) + 1

    endp = list(endp_counter.values())
    end_mean = mean(endp)
    end_stdev = pstdev(endp)

    if end_mean >= 2:
        res["durchEndp"] = 2
    if end_stdev <= 10:
        res["stdevEndp"] = 1

    return res


def get_DF(roh):
    res = {
        "durchDF": 0,
        "stdevDF": 0
    }

    df_counter = {}
    for data in roh:
        if all([data["dateiTypReal"], data["dateiTypReal"] != 1]):
            if data["metaDatensatz"] not in df_counter:
                df_counter[data["metaDatensatz"]] = {data["dateiTypReal"]}
            else:
                df_counter[data["metaDatensatz"]].add(data["dateiTypReal"])

    df = [len(df_counter[d]) for d in df_counter]
    df_mean = mean(df)
    df_stdev = pstdev(df)

    if df_mean >= 2:
        res["durchDF"] = 2
    if df_stdev <= 10:
        res["stdevDF"] = 1

    return res

def get_mean_tags(meta):
    res = 0

    t = mean([len(literal_eval(data["tags"])) for data in meta])

    if t >= 2:
        res = 2

    return res


def get_stdev_tags(meta):
    res = 0

    t = [tag for data in meta for tag in literal_eval(data["tags"]) if tag != 999999999]

    t_count = dict()
    for tag in t:
        t_count[tag] = t_count.get(tag, 0) + 1

    def_tags = pstdev(list(t_count.values()))

    if def_tags <= 10:
        res = 1

    return res


def get_ant_org(meta):
    res = 0

    publisher = set(data["organisation"] for data in meta if data["organisation"] != 1)
    anteil = len(publisher)/len(meta)

    if anteil >= 0.01:
        res += 1

    return res


def get_stdev_org(meta):
    res = 0

    o = [data["organisation"] for data in meta if data["organisation"] != 1]

    if o:
        o_count = dict()
        for org in o:
            o_count[org] = o_count.get(org, 0) + 1

        dev_orgs = pstdev(list(o_count.values()))

        if dev_orgs <= 10:
            res = 1

    return res


def get_div(meta, roh, portal):
    endp = get_end(roh)
    df = get_DF(roh)

    res = {
        "durchEndp": endp["durchEndp"],
        "stdevEndp": endp["stdevEndp"],
        "durchDF": df["durchDF"],
        "stdevDF": df["stdevDF"],
        "durchTags": get_mean_tags(meta),
        "stdevTags": get_stdev_tags(meta),
        "anteilOrg": get_ant_org(meta),
        "stdevOrg": get_stdev_org(meta)
    }

    res["score"] = calc_score(res)
    res["gewScore"] = res["score"]*5

    res["portalID"] = portal

    return res

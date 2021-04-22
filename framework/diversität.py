from statistics import mean, median, pvariance, pvariance
from ast import literal_eval
from framework.utility.scores import calc_score


def get_end(roh):
    """
    Berechnet die Metriken für die durchschnittliche Anzahl an Rohdaten pro Metadatensatz sowie deren Varianz
    """
    res = {
        "durchEndp": 0,
        "varianceEndp": 0
    }

    endp_counter = {}

    for data in roh:
        endp_counter[data["metaDatensatz"]] = endp_counter.get(data["metaDatensatz"], 0) + 1

    endp = list(endp_counter.values())
    end_mean = mean(endp)
    end_variance = pvariance(endp)

    if end_mean >= 2:
        res["durchEndp"] = 2
    if end_variance <= 4:
        res["varianceEndp"] = 1

    return res


def get_DF(roh):
    """
    Überprüft, ob durchschnittlich zwei oder mehr verschiedene Dateitypen pro Datensatz angeboten werden und
    ob die Varianz der Anzahlen der verschiedenen Dateitypen pro Datensatz kleiner oder gleich vier ist.
    """
    res = {
        "durchDF": 0,
        "varianceDF": 0
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
    df_variance = pvariance(df)

    if df_mean >= 2:
        res["durchDF"] = 2
    if df_variance <= 4:
        res["varianceDF"] = 1

    return res


def get_mean_tags(meta):
    """
    Überprüft, ob durchschnittlich zwei oder mehr verschiedene Tags pro Datensatz angegeben sind.
    """
    res = 0

    t = mean([len(literal_eval(data["tags"])) for data in meta])

    if t >= 2:
        res = 2

    return res


def get_variance_tags(meta):
    """
    Überprüft, ob die Varianz der Anzahlen der vergebenen Tags pro Datensatz kleiner oder gleich vier ist.
    """
    res = 0

    t = [tag for data in meta for tag in literal_eval(data["tags"]) if tag != 999999999]

    t_count = dict()
    for tag in t:
        t_count[tag] = t_count.get(tag, 0) + 1

    def_tags = pvariance(list(t_count.values()))

    if def_tags <= 4:
        res = 1

    return res


def get_ant_org(meta):
    """
    Überprüft ob die Anzahl an einzigartigen Organisationen, die für Datensätze angegeben wurden,
    mehr als ein Prozent der Anzahl an Datensätzen beträgt.
    """
    res = 0

    publisher = set(data["organisation"] for data in meta if data["organisation"] != 1)
    anteil = len(publisher)/len(meta)

    if anteil >= 0.01:
        res = 0.5

    return res


def get_variance_org(meta):
    """
    Überprüft, ob die Varianz der Häufigkeiten der Nutzung aller einzigartiger Organisationen in Datensätzen kleiner oder gleich zehn ist.
    """
    res = 0

    o = [data["organisation"] for data in meta if data["organisation"] != 1]

    if o:
        o_count = dict()
        for org in o:
            o_count[org] = o_count.get(org, 0) + 1

        dev_orgs = pvariance(list(o_count.values()))

        if dev_orgs <= 10:
            res = 0.5

    return res


def get_div(meta, roh, portal):
    """
    Berechnet die Werte der Metriken in der Dimension Diversität.
    :param roh: Rohdateninformationen eines OGD-Portals
    :param portal: Portal-ID
    :return: Die bestimmten Metrik-Werte der Dimension in einem Dictionary
    """
    endp = get_end(roh)
    df = get_DF(roh)

    res = {
        "durchEndp": endp["durchEndp"],
        "varianceEndp": endp["varianceEndp"],
        "durchDF": df["durchDF"],
        "varianceDF": df["varianceDF"],
        "durchTags": get_mean_tags(meta),
        "varianceTags": get_variance_tags(meta),
        "anteilOrg": get_ant_org(meta),
        "varianceOrg": get_variance_org(meta)
    }

    res["score"] = calc_score(res)
    res["gewScore"] = res["score"]*0.5

    res["portalID"] = portal

    return res

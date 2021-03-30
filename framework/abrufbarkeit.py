from statistics import mean
from framework.utility.scores import calc_score


def get_abr(rohdaten, portal_domain, portal):
    res = {
        "linkOnline": mean([9 if data["online"] == "True" else 0 for data in rohdaten]),
        "linkIntern": mean([1 if portal_domain in data["link"] else 0 for data in rohdaten]),
    }

    res["score"] = calc_score(res)
    res["gewScore"] = res["score"]

    res["portalID"] = portal

    return res

from statistics import mean
from framework.utility.scores import calc_score


def get_rue(meta):
    res = {
        "quelle": mean([10 if data["organisation"] != 1 else 0 for data in meta])
    }

    res["score"] = calc_score(res)
    res["gewScore"] = res["score"]*0.3

    return res

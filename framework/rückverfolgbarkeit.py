from statistics import mean


def get_rue(meta):
    res = {
        "quelle": mean([10 if data["organisation"] != 1 else 0 for data in meta])
    }

    return res

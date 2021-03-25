from statistics import mean


def get_abr(rohdaten, portal_domain):
    res = {
        "linkOnline": mean([9 if data["online"] == "True" else 0 for data in rohdaten]),
        "lintIntern": mean([1 if portal_domain in data["link"] else 0 for data in rohdaten]),
    }

    return res

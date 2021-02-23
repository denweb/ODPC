import json


def map_country(organization):
    country = ""
    try:
        if "country" in organization:
            if "id" in organization["country"]:
                country = country_mapping[organization["country"]["id"].upper()]
    except KeyError:
        pass
    return country


# read needed mapping-files
with open("transformer/resources/iso3.json", "r", encoding="iso-8859-1") as f:
    country_mapping = json.load(f)

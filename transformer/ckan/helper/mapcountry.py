import json


# NOT USED AT THE MOMENT! European data portal is mapped differently now.
def map_country(org_title):
    """
    Takes the catalogue-title of a ckan-dataitem to map to the corresponding country in ISO-3-format.
    For the europeandataportal.org.
    :param org_title: ["organization"]["title"]-information of a ckan dataitem.
    :return: The ISO-3 Code of the mapped country. Or "N/A" if none is found.
    """
    if org_title is not None:

        if org_title.startswith(" "):
            org_title = org_title[1:]

        title_lower = org_title.lower()

        if title_lower in country_mapping:
            return country_mapping[title_lower]
        else:
            return ""
    else:
        return ""


# read needed mapping-files
with open("transformer/resources/Countries Mapping.json", "r", encoding="iso-8859-1") as f:
    country_mapping = json.load(f)

country_mapping = {key.lower(): country_mapping[key] for key in country_mapping}

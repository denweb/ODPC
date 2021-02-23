import json


def remap_license(dataitem):
    """
    Maps the license-information given in a ckan-dataitem to the advaneo-license-format.
    :param dataitem: A dictionary containing a dataitem in ckan-format
    :return: a list with the license-information in advaneo-format. "N/A" as values if nothing is matched.
    """
    input_license_information = []
    fields = ["license_id", "license_url", "license_title"]

    for field in fields:
        if field in dataitem:
            if dataitem[field] is not None:
                if all([dataitem[field] != "N/A", dataitem[field] != "notspecified",
                        "other" not in dataitem[field].lower()]):
                    input_license_information.append(dataitem[field].lower())

    if input_license_information:
        # check if license-information is in mapping-file
        for license in license_mapping["licenses"]:
            for input_license_field in input_license_information:
                if any([input_license_field in license["id"].lower(),
                        input_license_field in license["title"].lower(),
                        input_license_field in license["url"].lower(),
                        input_license_field in license["mappings"].lower()]
                       ):
                    # return mapped license information on any hit
                    return[{
                        "id": license["id"],
                        'licenseId': license["id"],
                        "licenseTitle": license["title"],
                        "licenseUrl": license["url"],
                        }]
        # return N/A on no hit
        return [{
                "id": "N/A",
                'licenseId': "N/A",
                "licenseTitle": "N/A",
                "licenseUrl": "N/A",
                }]
    else:
        # return N/A if no license-information is given in the dataitem
        return [{
                "id": "N/A",
                'licenseId': "N/A",
                "licenseTitle": "N/A",
                "licenseUrl": "N/A",
                }]


with open("transformer/resources/licences.json", "r", encoding="utf-8") as f:
    license_mapping = json.load(f)
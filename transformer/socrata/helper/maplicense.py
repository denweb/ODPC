import json


def remap_license(licenseurl):
    """
    Maps the license-information given in a socrata-dataitem to the advaneo-license-format.
    :return: a list with the license-information in advaneo-format. "N/A" as values if nothing is matched.
    """

    if all([licenseurl != "N/A", licenseurl is not None, licenseurl != ""]):
        # check if license-information is in mapping-file
        for license in license_mapping["licenses"]:
            if any([licenseurl in license["id"].lower(),
                    licenseurl in license["title"].lower(),
                    licenseurl in license["url"].lower(),
                    licenseurl in license["mappings"].lower()]
                   ):
                # return mapped license information on any hit
                return[{
                    "id": license["id"],
                    'licenseId': license["id"],
                    "licenseTitle": license["title"],
                    "licenseUrl": license["url"],
                }]
        # return N/A on no hit
        return [
            {
                "id": licenseurl,
                'licenseId': licenseurl,
                "licenseTitle": licenseurl,
                "licenseUrl": licenseurl,
            }]
    else:
        # return N/A if no license-information is given in the dataitem
        return [
            {
                "id": "N/A",
                'licenseId': "N/A",
                "licenseTitle": "N/A",
                "licenseUrl": "N/A",
            }]


with open("transformer/resources/licences.json", "r", encoding="utf-8") as f:
    license_mapping = json.load(f)

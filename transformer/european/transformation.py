from transformer.helper.mapcategories import remap_categories
from transformer.european.helper.maplicense import remap_license
from transformer.helper.removehtmltags import remove_html_tags
from transformer.european.helper.mapcountry import map_country
from transformer.helper.transformkeywords import transform_keywords
from transformer.european.helper.getmail import get_mail
from transformer.helper.getdomain import get_domain
from transformer.european.helper.mapdataendpoint import map_dataendpoint
from transformer.european.helper.getauthmain import get_authmain
from transformer.european.helper.geturl import get_url


def remap(dataitem, portal_id):
    """
    Takes the metadata-information of a dataitem in euro-format and remaps it to the advaneo-format. Directly checks
    for url-statuts and returns None, if the dataitem has neither title, id now dataendpoints.
    :param dataitem: A dictionary representing a dataitem in ckan-format
    :return: A dictionary representing a dataitem in advaneo-format. Or None if the requirements are not met.
    """
    # check for missing values in dataitem
    checklist = ["organization", "version"]

    # check if dataitem has a title and DataEndpoints
    if all(["translation" in dataitem, "id" in dataitem, "resources" in dataitem]):
        if all([dataitem["translation"], dataitem["resources"]]):

            for field in checklist:
                if field not in dataitem:
                    dataitem[field] = "N/A"
                elif dataitem[field] is None:
                    dataitem[field] = "N/A"
                elif dataitem[field] == "":
                    dataitem[field] = "N/A"
                elif dataitem[field] == " ":
                    dataitem[field] = "N/A"

            language = list(dataitem["translation"])[0]

            output = {
                "uuid": dataitem["id"],
                "title": remove_html_tags(dataitem["translation"][language]["title"]),
                "privateData": False,
                "author": get_authmain(dataitem, "author"),
                "authorEmail": get_mail(dataitem, "author"),
                "maintainer": get_authmain(dataitem, "maintainer"),
                "maintainerEmail": get_mail(dataitem, "maintainer"),
                "description": remove_html_tags(dataitem["translation"][language]["notes"]),
                "providerUrl": get_url(dataitem["organization"]),
                "state": "ACTIVE",
                "type": "DATA_SET",
                "privacyMode": "NOT_CONFIDENTIAL",
                "rating": 0,
                "garbage": [],
                "keywords": transform_keywords(dataitem["tags"], "european"),
                "categories": remap_categories(dataitem["tags"]),
                "dataEndpoints": [map_dataendpoint(endpoint) for endpoint in dataitem['resources']],
                "organization": {"id": "59314f3a00240a000e0c2113",
                                 "name": "Test company name"
                                 },
                "licenses": remap_license(dataitem),
                "geoGranularity": "CONTINENT",
                "variability": "STRUCTURED_DATA",
                "paymentModel": "FREE_OF_CHARGE",
                "period": "N/A",
                "characteristics": [
                    "VOLUME",
                    "VELOCITY"
                ],
                "images": [
                    "img1"
                ],
                "termsOfUse": {
                    "freeText": "---",
                    "openDataLicenseId": "---",
                    "exclusivity": "NON_EXCLUSIVE_USAGE",
                    "startDate": "2017-08-29T06:22:43.028+0000",
                    "endDate": "2017-08-29T06:22:43.028+0000",
                    "geoRestriction": False,
                    "timeRestriction": False,
                    "freeToUse": False
                },
                "country": map_country(dataitem["organization"])
                # "version": "NA",
            }

            # check for providerUrl
            if output["providerUrl"] == "N/A":
                output["providerUrl"] = get_domain(output["dataEndpoints"][0]["url"])

            return output
        else:
            return None
    else:
        return None

from transformer.helper.mapcategories import remap_categories
from transformer.helper.getdomain import get_domain
from transformer.helper.removehtmltags import remove_html_tags
from transformer.arcgis.helper.mapdataendpoint import map_dataendpoint
from transformer.helper.transformkeywords import transform_keywords
from transformer.helper.transormgarbage import transform_garbage
from transformer.helper.transformmail import transform_mail
from transformer.helper.getid import get_id


def remap(dataitem):

    # check for missing values in dataitem
    checklist = ['identifier', 'issued', 'modified', 'publisher',
                 'accessLevel', 'distribution', 'landingPage', 'webService', 'license',
                 'spatial', 'theme']

    # check if dataitem has a title and DataEndpoints
    if all(["title" in dataitem, "distribution" in dataitem]):

        for field in checklist:
            if field not in dataitem:
                dataitem[field] = "NA"
            elif dataitem[field] is None:
                dataitem[field] = "N/A"
            elif not dataitem[field]:
                dataitem[field] = "N/A"

        # catch faulty contact-information
        if "contactPoint" in dataitem:
            if "fn" not in dataitem["contactPoint"]:
                dataitem["contactPoint"]["fn"] = "N/A"

            if "hasEmail" not in dataitem["contactPoint"]:
                dataitem["contactPoint"]["hasEmail"] = "N/A"
        else:
            dataitem["contactPoint"] = {"fn": "N/A", "hasEmail": "N/A"}

            # transform keywords beforehand for late convenience
            if "keyword" in dataitem:
                dataitem["keyword"] = transform_keywords(dataitem["keyword"], "arcgis")
            else:
                dataitem["keyword"] = []

        output = {
            "uuid": get_id(dataitem["identifier"]),
            "title": remove_html_tags(dataitem["title"]),
            "privateData": False,
            "author": dataitem["contactPoint"]["fn"],
            "authorEmail": transform_mail(dataitem["contactPoint"]["hasEmail"]),
            "maintainer": dataitem["contactPoint"]["fn"],
            "maintainerEmail": transform_mail(dataitem["contactPoint"]["hasEmail"]),
            "description": remove_html_tags(dataitem["description"]),
            "providerUrl": get_domain(dataitem["identifier"]),
            "state": "ACTIVE",
            "type": "DATA_SET",
            "privacyMode": "NOT_CONFIDENTIAL",
            "rating": 0,
            "garbage": transform_garbage({
                "accessLevel": dataitem["accessLevel"],
                "publisher": dataitem["publisher"],
                "landingPage": dataitem["landingPage"],
                "webService": dataitem["webService"],
                "theme": dataitem["theme"]
            },
                "arcgis"),
            "keywords": dataitem['keyword'],
            "categories": remap_categories(dataitem["keyword"]),
            "dataEndpoints": [map_dataendpoint(endpoint, dataitem) for endpoint in dataitem['distribution']],
            "organization": {"id": "592eabfc076d050012355c8a",
                             "name": "Advaneo Data Marketplace",
                             "logo": {
                                 "id": "5ac743693dd5610015b36a05"}
                             },
            "licenses": [
                {
                    "id": "ARCGIS",
                    'licenseId': "ARCGIS",
                    "licenseTitle": "ArcGIS Open Data License",
                    "licenseUrl": "https://creativecommons.org/licenses/",
                }],
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
            "country": "",  # map dataitem["spatial"] here
            # "version": "NA",
        }

        return output
    else:
        return None

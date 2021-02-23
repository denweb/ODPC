from transformer.helper.mapcategories import remap_categories
from transformer.helper.getdomain import get_domain
from transformer.helper.removehtmltags import remove_html_tags
from transformer.arcgis.helper.mapdataendpoint import map_dataendpoint
from transformer.helper.transformkeywords import transform_keywords
from transformer.helper.transormgarbage import transform_garbage
from transformer.helper.transformmail import transform_mail
from transformer.helper.getid import get_id
from transformer.helper.transformorganisation import transform_organisation
from transformer.helper.transformdate import transform_date
from transformer.helper.transformgroup import transform_group


def remap(dataitem, portal_id):

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
                dataitem["contactPoint"]["fn"] = None

            if "hasEmail" not in dataitem["contactPoint"]:
                dataitem["contactPoint"]["hasEmail"] = None
        else:
            dataitem["contactPoint"] = {"fn": None, "hasEmail": None}

        # transform keywords beforehand for convenience
        if "keyword" in dataitem:
            dataitem["keyword"] = transform_keywords(dataitem["keyword"], "arcgis")
        else:
            dataitem["keyword"] = []

        # Todo: extra
        output = {
            "titel": remove_html_tags(dataitem["title"]),
            "beschreibung": remove_html_tags(dataitem["description"]),
            "autor": {
                "kontaktName": dataitem["contactPoint"]["fn"],
                "kontaktEmail": transform_mail(dataitem["contactPoint"]["hasEmail"])
            },
            "verwalter": {
                "kontaktName": dataitem["contactPoint"]["fn"],
                "kontaktEmail": transform_mail(dataitem["contactPoint"]["hasEmail"])
            },
            "url": dataitem["landingPage"],
            "geo": dataitem["spatial"],
            "organisation": transform_organisation("arcgis", dataitem["publisher"]),
            "erstellDatum": transform_date(dataitem["issued"], "ckan"),
            "updateDatum": transform_date(dataitem["modified"], "ckan"),
            "gruppen": [],
            "extra": None,
            "lizenz": {
                "lizenzTitel": None,
                "lizenzUrl": dataitem["license"]
            },
            "tags": dataitem["keyword"],
            "kategorien": [],
            "portalID": portal_id,
            "endpunkte": [map_dataendpoint(endpoint, dataitem) for endpoint in dataitem['distribution']]
        }

        return output
    else:
        return None

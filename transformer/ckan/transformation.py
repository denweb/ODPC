from transformer.helper.mapcategories import remap_categories
from transformer.ckan.helper.maplicense import remap_license
from transformer.helper.removehtmltags import remove_html_tags
from transformer.helper.transformkeywords import transform_keywords
from transformer.helper.transormgarbage import transform_garbage
from transformer.helper.transformmail import transform_mail
from transformer.helper.getdomain import get_domain
from transformer.ckan.helper.mapdataendpoint import map_dataendpoint
from transformer.helper.transformorganisation import transform_organisation
from transformer.helper.transformdate import transform_date
from transformer.helper.transformgroup import transform_group


def remap(dataitem, portal_id):
    """
    Takes the metadata-information of a dataitem in ckan-format and remaps it to the advaneo-format. Directly checks
    for url-statuts and returns None, if the dataitem has neither title, id now dataendpoints.
    :param dataitem: A dictionary representing a dataitem in ckan-format
    :return: A dictionary representing a dataitem in advaneo-format. Or None if the requirements are not met.
    """
    # check for missing values in dataitem
    checklist = ["title", "author", "author_email", "maintainer", "maintainer_email", "license_id", "license_title", "license_url",
                 "notes", "url", "type", "organization", "metadata_created", "metadata_modified"]

    for field in checklist:
        if field not in dataitem:
            dataitem[field] = None
        elif dataitem[field] == "":
            dataitem[field] = None
        elif dataitem[field] == " ":
            dataitem[field] = None

    # check if array-attributes are given
    if "extras" in dataitem:
        dataitem["extras"] = transform_garbage(dataitem["extras"], "ckan")
    else:
        dataitem["extras"] = None

    if "tags" in dataitem:
        dataitem["tags"] = transform_keywords(dataitem["tags"], "ckan")
    else:
        dataitem["tags"] = []

    if "groups" in dataitem:
        dataitem["groups"] = [transform_group(gruppe, "ckan") for gruppe in dataitem["groups"]]
    else:
        dataitem["groups"] = []

    if "resources" in dataitem:
        dataEndpoints = [map_dataendpoint(endpoint) for endpoint in dataitem['resources']]
    else:
        dataEndpoints = []

    # Todo: Kategorie, extras (+ fixen!)
    output = {
        "titel": remove_html_tags(dataitem["title"]),
        "beschreibung": remove_html_tags(dataitem["notes"]),
        "autor": {
            "kontaktName": dataitem["author"],
            "kontaktEmail": dataitem["author_email"]
        },
        "verwalter": {
            "kontaktName": dataitem["maintainer"],
            "kontaktEmail": dataitem["maintainer_email"]
        },
        "url": dataitem["url"],
        "geo": None,
        "organisation": transform_organisation("ckan", dataitem["organization"]),
        "erstellDatum": transform_date(dataitem["metadata_created"], "ckan"),
        "updateDatum": transform_date(dataitem["metadata_modified"], "ckan"),
        "gruppen": dataitem["groups"],
        "extra": None,
        "lizenz": {
            "lizenzTitel": dataitem["license_title"],
            "lizenzUrl": dataitem["license_url"]
        },
        "tags": dataitem["tags"],
        "kategorien": [],
        "portalID": portal_id,
        "endpunkte": dataEndpoints
    }

    return output

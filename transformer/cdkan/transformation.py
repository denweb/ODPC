from transformer.helper.removehtmltags import remove_html_tags
from transformer.helper.transformkeywords import transform_keywords
from transformer.helper.transormgarbage import transform_garbage
from transformer.cdkan.helper.mapdataendpoint import map_dataendpoint
from transformer.helper.transformorganisation import transform_organisation
from transformer.helper.transformdate import transform_date
from transformer.helper.transformgroup import transform_group


def remap(dataitem, portal_id):
    """
    Transformiert die Metadaten eines gesamten Datensatzes im CKAN und DKAN-Format
    in das standardisierte Format dieser Arbeit.
    :param dataitem: Die Metadaten zum Datensatz (Dictionary)
    :param portal_id: Die ID des Portals in der Daten-DB
    :return: Der transformierte Datensatz (Dictionary)
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
        dataitem["extras"] = transform_garbage(dataitem["extras"], "cdkan")
    else:
        dataitem["extras"] = None

    if "tags" in dataitem:
        dataitem["tags"] = transform_keywords(dataitem["tags"], "cdkan")
    else:
        dataitem["tags"] = []

    if "groups" in dataitem:
        dataitem["groups"] = [transform_group(gruppe, "cdkan") for gruppe in dataitem["groups"]]
    else:
        dataitem["groups"] = []

    if "resources" in dataitem:
        dataEndpoints = [map_dataendpoint(endpoint) for endpoint in dataitem['resources']]
    else:
        dataEndpoints = []

    # Todo: Kategorie, extras
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
        "organisation": transform_organisation("cdkan", dataitem["organization"]),
        "erstellDatum": transform_date(dataitem["metadata_created"], "cdkan"),
        "updateDatum": transform_date(dataitem["metadata_modified"], "cdkan"),
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

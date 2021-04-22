from transformer.helper.removehtmltags import remove_html_tags
from transformer.arcgis.helper.mapdataendpoint import map_dataendpoint
from transformer.helper.transformkeywords import transform_keywords
from transformer.helper.transformorganisation import transform_organisation
from transformer.helper.transformdate import transform_date


def remap(dataitem, portal_id):
    """
    Transformiert die Metadaten eines gesamten Datensatzes im Arcgis-Format in das standardisierte Format dieser Arbeit.
    :param dataitem: Die Metadaten zum Datensatz (Dictionary)
    :param portal_id: Die ID des Portals in der Daten-DB
    :return: Der transformierte Datensatz (Dictionary)
    """

    # check for missing values in dataitem
    checklist = ['title', 'identifier', 'issued', 'modified', 'publisher',
                 'accessLevel', 'distribution', 'landingPage', 'webService', 'license',
                 'spatial', 'theme']

    for field in checklist:
        if field not in dataitem:
            dataitem[field] = None

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

    if "distribution" in dataitem:
        dataEndpoints = [map_dataendpoint(endpoint, dataitem) for endpoint in dataitem['distribution']]
    else:
        dataEndpoints = []

    # Todo: extra
    output = {
        "titel": remove_html_tags(dataitem["title"]),
        "beschreibung": remove_html_tags(dataitem["description"]),
        "autor": {
            "kontaktName": dataitem["contactPoint"]["fn"],
            "kontaktEmail": dataitem["contactPoint"]["hasEmail"]
        },
        "verwalter": {
            "kontaktName": dataitem["contactPoint"]["fn"],
            "kontaktEmail": dataitem["contactPoint"]["hasEmail"]
        },
        "url": dataitem["landingPage"],
        "geo": dataitem["spatial"],
        "organisation": transform_organisation("arcgis", dataitem["publisher"]),
        "erstellDatum": transform_date(dataitem["issued"], "cdkan"),
        "updateDatum": transform_date(dataitem["modified"], "cdkan"),
        "gruppen": [],
        "extra": None,
        "lizenz": {
            "lizenzTitel": None,
            "lizenzUrl": dataitem["license"]
        },
        "tags": dataitem["keyword"],
        "kategorien": [],
        "portalID": portal_id,
        "endpunkte": dataEndpoints
    }

    return output

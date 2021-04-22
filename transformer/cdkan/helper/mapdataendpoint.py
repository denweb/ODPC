from transformer.helper.removehtmltags import remove_html_tags
from transformer.helper.transformdate import transform_date


def map_dataendpoint(endpoint):
    """
    Transformiert die Metadaten zu den Rohdaten eines CKAN oder DKAN-Datensatzes in das standardisierte Format.
    :param endpoint: Die Metadaten des Rohdatensatzes (Dictionary)
    :return: Die transformierten Metadaten (Dictionary)
    """

    # check for missing values in input
    endpoint_checklist = ["hash", "description", "format", "name", "resource_type", "mimetype", "mimetype_inner",
                          "cache_url", "created", "last_modified", "cache_last_updated", "upload", "package_id"]

    for field in endpoint_checklist:
        if field not in endpoint:
            endpoint[field] = None
        elif all([field in endpoint, not endpoint[field]]):
            endpoint[field] = None
        elif all([field in endpoint, endpoint[field] == ""]):
            endpoint[field] = None
        elif all([field in endpoint, endpoint[field] == " "]):
            endpoint[field] = None

    # Todo: extras
    # map to standard format
    new_endpoint = {
        "link": endpoint["url"],
        "online": False,
        "dateiName": remove_html_tags(endpoint["name"]),
        "valide": None,
        "beschreibung": endpoint["description"],
        "dateiTyp": endpoint["resource_type"],
        "dateiGröße": 0,
        "titel": None,
        "erstellDatum": transform_date(endpoint["created"], "cdkan"),
        "updateDatum": transform_date(endpoint["last_modified"], "cdkan"),
        "metaDatensatz": 1,
        "extras": None
    }

    return new_endpoint

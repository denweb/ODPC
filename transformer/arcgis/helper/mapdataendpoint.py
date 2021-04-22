from transformer.helper.removehtmltags import remove_html_tags
from transformer.helper.transformdate import transform_date


def map_dataendpoint(endpoint, input):
    """
    Transformiert die Metadaten zu den Rohdaten eines Arcgis-Datensatzes in das standardisierte Format.
    :param endpoint: Die Metadaten des Rohdatensatzes (Dictionary)
    :param input: Die Metadateniformationen des beinhaltenden Datensatzes (Dictionary)
    :return: Die transformierten Metadaten (Dictionary)
    """

    # check for missing values in input
    endpoint_checklist = ["title", "format", "mediaType", "size"]
    for field in endpoint_checklist:
        if field not in endpoint:
            endpoint[field] = None
        elif all([field in endpoint, not endpoint[field]]):
            endpoint[field] = None

    # map to new array/dict
    # Todo: Extras
    new_endpoint = {
        "link": None,
        "online": False,
        "dateiName": remove_html_tags(endpoint["title"]),
        "valide": None,
        "beschreibung": None,
        "dateiTyp": endpoint["mediaType"].upper(),
        "dateiGröße": 0,
        "titel": None,
        "erstellDatum": transform_date(input["issued"], "arcgis"),
        "updateDatum": transform_date(input["modified"], "arcgis"),
        "metaDatensatz": 1,
        "extras": None
    }

    # check, if  its "accessURL" or "downloadURL"
    if "accessURL" in endpoint:
        new_endpoint["link"] = endpoint["accessURL"]
    elif "downloadURL" in endpoint:
        new_endpoint["link"] = endpoint["downloadURL"]

    return new_endpoint

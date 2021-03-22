import datetime
import uuid
import requests
from transformer.helper.removehtmltags import remove_html_tags
from utility.websiteInfo import check_all
from utility.utility import get_connection
from transformer.helper.transformdate import transform_date


def map_dataendpoint(endpoint):

    # check for missing values in input
    endpoint_checklist = ["hash", "description", "format", "name", "resource_type", "mimetype", "mimetype_inner", "cache_url",
                          "created", "last_modified", "cache_last_updated", "upload", "package_id"]

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
        "erstellDatum": transform_date(endpoint["created"], "ckan"),
        "updateDatum": transform_date(endpoint["last_modified"], "ckan"),
        "metaDatensatz": 1,
        "extras": "Ne"
    }

    """
    # check if date-information is given
    # Wird das gebraucht? Glaube fast nicht.
    if endpoint["created"]:
        new_endpoint["erstellDatum"] = transform_date(endpoint["created"], "ckan")
    else:
        new_endpoint["erstellDatum"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+"+0000"

    if endpoint["last_modified"]:
        new_endpoint["updateDatum"] = transform_date(endpoint["last_modified"], "ckan")
    elif all([endpoint["last_modified"] == "N/A", endpoint["created"] != "N/A"]):
        new_endpoint["updateDatum"] = transform_date(endpoint["created"], "ckan")
    elif all([endpoint["last_modified"] == "N/A", endpoint["created"] == "N/A"]):
        new_endpoint["updateDatum"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "+0000"
    """

    return new_endpoint

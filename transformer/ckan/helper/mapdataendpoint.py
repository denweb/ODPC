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


    # Todo: extras, default online Status bestimmen
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

    # check if date-information is given
    if endpoint["created"] != "N/A":
        new_endpoint["erstellDatum"] = transform_date(endpoint["created"], "ckan")
    else:
        new_endpoint["erstellDatum"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+"+0000"
    if endpoint["last_modified"] != "N/A":
        new_endpoint["updateDatum"] = transform_date(endpoint["last_modified"], "ckan")
    elif all([endpoint["last_modified"] == "N/A", endpoint["created"] != "N/A"]):
        new_endpoint["updateDatum"] = transform_date(endpoint["created"], "ckan")
    elif all([endpoint["last_modified"] == "N/A", endpoint["created"] == "N/A"]):
        new_endpoint["updateDatum"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "+0000"

    #Todo: Beim Rohdaten-Check auktualisieren, da dort eh alles getestet wird.
    """
    # check the url-status
    response = get_connection(endpoint["url"])
    if isinstance(response, requests.Response):
        url_data = check_all(response)
        response.close()
    else:
        url_data = {'url_status': "404"}

    # update values for the endpoint
    if url_data['url_status'] == "200, OK":
        new_endpoint["online"] = True
        new_endpoint["dateiGröße"] = url_data['size']
        new_endpoint["dateiTyp"] = url_data['ext']
    else:
        new_endpoint["online"] = False
    """

    return new_endpoint

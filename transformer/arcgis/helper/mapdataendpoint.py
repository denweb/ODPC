from transformer.helper.getid import get_id
import requests
from transformer.helper.removehtmltags import remove_html_tags
from utility.websiteInfo import check_all
from utility.utility import get_connection
from transformer.helper.transformdate import transform_date


def map_dataendpoint(endpoint, input):

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
        "extras": "Ne"
    }

    # check, if  its "accessURL" or "downloadURL"
    if "accessURL" in endpoint:
        new_endpoint["link"] = endpoint["accessURL"]
        #response = get_connection(endpoint["accessURL"])
    elif "downloadURL" in endpoint:
        new_endpoint["link"] = endpoint["downloadURL"]
        #response = get_connection(endpoint["downloadURL"])
    else:
        response = None

    """
    if isinstance(response, requests.Response):
        url_data = check_all(response)
        response.close()
    else:
        url_data = {'url_status': "404"}

    # update values for the endpoint
    if url_data['url_status'] == "200, OK":
        new_endpoint["active"] = True
        new_endpoint["size"] = url_data['size']
        new_endpoint["mimeType"] = url_data['mimetype']
        new_endpoint["dataFormat"] = url_data['ext']
    else:
        new_endpoint["active"] = False
    """

    return new_endpoint

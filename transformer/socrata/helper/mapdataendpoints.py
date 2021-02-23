from transformer.helper.getid import get_id
import requests
from transformer.helper.removehtmltags import remove_html_tags
from utility.websiteInfo import check_all
from utility.utility import get_connection
from transformer.helper.transformdate import transform_date


def map_dataendpoint(endpoint, modified):

    # check for missing values in input
    endpoint_checklist = ["title", "format", "mediaType", "size"]
    for field in endpoint_checklist:
        if field not in endpoint:
            endpoint[field] = "N/A"
        elif all([field in endpoint, endpoint[field] is None]):
            endpoint[field] = "N/A"
        elif all([field in endpoint, not endpoint[field]]):
            endpoint[field] = "N/A"

    # map to new array/dict
    new_endpoint = {
        "key": get_id(""),
        "url": "",
        "description": endpoint["title"],
        "dataFormat": endpoint["format"].upper(),
        "hash": "2395473570342502734",
        "name": remove_html_tags(endpoint["title"]),
        "mimeType": endpoint["mediaType"].upper(),
        "mimeTypeInner": "",
        "size": 0,
        "created": transform_date(modified, "socrata"),
        "lastModified": transform_date(modified, "socrata"),
        "active": True,
        "available": True,
        "dataThroughput": 0,
        "updates": "OTHERS",
        "extData": [
           {
             "key": "",
             "value": ""
           }
         ],
        "contracts": [
           {
             "price": 0,
             "currency": "EUR",
             "paymentType": "PAY_ONCE"
           }
         ]
    }

    # check, if  its "accessURL" or "downloadURL"
    if "accessURL" in endpoint:
        new_endpoint["url"] = endpoint["accessURL"]
        response = get_connection(endpoint["accessURL"])
    elif "downloadURL" in endpoint:
        new_endpoint["url"] = endpoint["downloadURL"]
        response = get_connection(endpoint["downloadURL"])
    else:
        response = None

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
    return new_endpoint

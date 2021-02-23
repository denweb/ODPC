import datetime
from transformer.helper.getid import get_id
import requests
from utility.websiteInfo import check_all
from utility.utility import get_connection
from transformer.helper.transformdate import transform_date


def map_dataendpoint(endpoint):
    # check for missing values in input
    endpoint_checklist = ["hash", "format", "mimetype", "mimetype_inner", "created", "last_modified", "id"]

    for field in endpoint_checklist:
        if field not in endpoint:
            endpoint[field] = "N/A"
        elif endpoint[field] is None:
            endpoint[field] = "N/A"
        elif not endpoint[field]:
            endpoint[field] = "N/A"
        elif endpoint[field] == "":
            endpoint[field] = "N/A"
        elif endpoint[field] == " ":
            endpoint[field] = "N/A"

    notes = "N/A"
    title = "N/A"

    if endpoint["translation"]:
        endpoint_lang = list(endpoint["translation"])[0]
        if "notes" in endpoint["translation"][endpoint_lang]:
            notes = endpoint["translation"][endpoint_lang]["notes"]

        if "title" in endpoint["translation"][endpoint_lang]:
            title = endpoint["translation"][endpoint_lang]["title"]

    if any([notes == "", notes is None]):
        notes = "N/A"
    if any([title == "", title is None]):
        title = "N/A"

    if endpoint["size"] is None:
        endpoint["size"] = 0

    # map to new array/dict
    new_endpoint = {
        "key": endpoint["id"],
        "url": endpoint["access_url"],
        "description": notes,
        "dataFormat": endpoint["format"].upper(),
        "hash": endpoint["hash"],
        "name": title,
        "mimeType": endpoint["mimetype"].upper(),
        "mimeTypeInner": endpoint["mimetype_inner"].upper(),
        "size": endpoint["size"],
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

    # check if key information is not N/A
    if new_endpoint["key"] == "N/A":
        new_endpoint["key"] = get_id("")

    # check if date-information is given
    if endpoint["created"] != "N/A":
        new_endpoint["created"] = transform_date(endpoint["created"])
    else:
        new_endpoint["created"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+"+0000"

    if endpoint["last_modified"] != "N/A":
        new_endpoint["lastModified"] = transform_date(endpoint["last_modified"])
    elif all([endpoint["last_modified"] == "N/A", endpoint["created"] != "N/A"]):
        new_endpoint["lastModified"] = transform_date(endpoint["created"])
    elif all([endpoint["last_modified"] == "N/A", endpoint["created"] == "N/A"]):
        new_endpoint["lastModified"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "+0000"

    # check the url-status
    response = get_connection(new_endpoint["url"])
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

import json


def get_dataitems(website_data, portal):
    """
    Returns the a list of the JSON-representation of every data-item of the OGD-Portal - if possible.
    :param website_data: Dictionary of the crawled JSON data.
    :param portal: String containing the kind of portal to be crawled.
    :return: A List with the JSON-representation of every data-Item.
    """

    try:
        if portal in ["cdkan", "european"]:
            return website_data['result']["results"]
        elif portal in ["socrata", "arcgis"]:
            return website_data['dataset']
        elif portal == "dkan":
            return website_data["result"][0]
        elif portal == "opendatasoft":
            return website_data["datasets"]
        else:
            return "Unknown portal"

    except:
        return "No JSON"

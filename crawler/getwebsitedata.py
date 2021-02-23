import json


def get_website_data(response):
    """
    Returns the number of data-items of the ARCGIS-Website - if possible.
    :param response: A response-object for the website to be harvested in the form "x.com/data.json"
    :return: An Integer with the number of data-items. Returns -1, if there is no JSON-file.
    """
    try:
        return json.loads(response.content.decode())
    except:
        return None


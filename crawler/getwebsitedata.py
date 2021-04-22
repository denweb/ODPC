import json


def get_website_data(response):
    """
    Returns the number of data-items of the OGD-Portal - if possible.
    :param response: A response-object for the website to be harvested.
    :return: An Integer with the number of data-items.
    """
    try:
        return json.loads(response.content.decode())
    except:
        return None


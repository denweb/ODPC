import requests
import sys


def set_limit_and_offset(argv):
    """
    Extracts offset and limit variables from the command line argument given to the crawler crawl.
    Both variables have to be set in to form of "offset=x" and "limit=x"
    :param argv: a list with two strings representing the offset and limit parameters
    :return: download_limit and offset variables as Integer-Values
    """

    # set both variables to zero in case one doesn't exist in the arguments
    download_limit, offset = 0, 0

    for arg in argv:
        if "limit" in arg.lower():
            download_limit = arg.split("=")[1]
            if download_limit.isdigit():
                download_limit = int(download_limit)
            else:
                print("Please enter a valid Integer as limit.")
                sys.exit()
        elif "offset" in arg:
            offset = arg.split("=")[1]
            if offset.isdigit():
                offset = int(offset)
            else:
                print("Please enter a valid Integer as offset.")
                sys.exit()

    return download_limit, offset


def get_connection(url, open_conn=False):
    """
    Establishes a streamed connection to a given URL.
    :param url:
    :param open_conn:
    :return: A Response-Object with
    """
    try:
        if not open_conn:
            with requests.get(url, verify=False, stream=True, timeout=60) as response:
                return response
        else:
            return requests.get(url, verify=False, stream=True, timeout=60)
    except requests.exceptions.ReadTimeout as e:
        return e
    except requests.exceptions.ConnectionError as e:
        return e
    except requests.exceptions.MissingSchema as e:
        return e
    except Exception as e:
        return e


def create_modlink(link, portal):
    modlink = ""

    if portal == "ckan":
        if not link.endswith("/"):
            modlink = "".join([link, "/api/3/action/package_search?rows={}&start={}"])
        else:
            modlink = "".join([link, "api/3/action/package_search?rows={}&start={}"])

    if portal == "european":
        if not link.endswith("/"):
            modlink = "".join([link, "/data/search/ckan/package_search?rows={}&start={}"])
        else:
            modlink = "".join([link, "data/search/ckan/package_search?rows={}&start={}"])

    if portal == "dkan":
        if not link.endswith("/"):
            modlink = "".join([link, "/api/3/action/current_package_list_with_resources"])
        else:
            modlink = "".join([link, "api/3/action/current_package_list_with_resources"])

    # opendatasoft eigene API v2 liefert nicht die benötigten Daten. Downloadlinks fehlen und metadaten sind teilweise falsch.
    # brauche datasetID und damit dann über resource_suche die richtigen Rohdaten finden. Wo sind die Links?!
    if portal == "opendatasoft":
        if not link.endswith("/"):
            modlink = "".join([link, "/api/v2/catalog/datasets?rows={}"])
        else:
            modlink = "".join([link, "api/v2/catalog/datasets?rows={}"])

    if portal in ["socrata", "arcgis"]:
        if not link.endswith("/"):
            modlink = "%s/data.json" % link
        else:
            modlink = "%sdata.json" % link

    return modlink

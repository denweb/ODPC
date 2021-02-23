from utility.utility import get_connection
from crawler.getwebsitedata import get_website_data
from utility.utility import create_modlink
from transformer.helper.getdomain import get_domain
import requests


def get_link_portal(link):
    if isinstance(link, str):
        pre = ["data.", "daten.", "transparenz.", "suche.", "ckan."]
        post = ["/dataset", "/data", "/daten"]

        domain = get_domain(link)

        # check given link as it is
        portal = assign(link)
        if portal != "unknown":
            return link, portal

        # check domain
        portal = assign(domain)
        if portal != "unknown":
            return domain, portal

        # check with prefixes
        # check for current prefix
        if all([domain.startswith("http://"), not domain.startswith("http://www.")]):
            pl = 7
        elif all([domain.startswith("https://"), not domain.startswith("https://www.")]):
            pl = 8
        elif domain.startswith("http://www."):
            pl = 11
        else:
            pl = 12

        # check for prefixes
        for prefix in pre:
            temp_link = "".join([domain[:pl], prefix, domain[pl:]])
            portal = assign(temp_link)

            if portal != "unknown":
                return temp_link, portal

        # check post-fixes
        for postfix in post:
            temp_link = "".join([domain, postfix])
            portal = assign(temp_link)

            if portal != "unknown":
                return temp_link, portal

    return link, "unknown"


# Todo: Make prettier / better
def assign(link):

    # check for arcgis
    if "arcgis" in link:
        return "arcgis"

    # Check for CKAN
    ckan_testlink = create_modlink(link, "ckan")

    response = get_connection(ckan_testlink.format(1, 0), open_conn=True)

    if isinstance(response, requests.Response):
        link_content = get_website_data(response)
        response.close()

        if isinstance(link_content, dict):
            if "result" in link_content:
                return "ckan"

    # check for DKAN
    dkan_testlink = create_modlink(link, "dkan")

    response = get_connection(dkan_testlink, open_conn=True)

    if isinstance(response, requests.Response):
        link_content = get_website_data(response)
        response.close()

        if isinstance(link_content, dict):
            if "success" in link_content:
                return "dkan"

    # check for opendatasoft
    ods_testlink = create_modlink(link, "opendatasoft")

    response = get_connection(ods_testlink.format(0), open_conn=True)

    if isinstance(response, requests.Response):
        link_content = get_website_data(response)
        response.close()

        if isinstance(link_content, dict):
            if "datasets" in link_content:
                return "opendatasoft"

    # check for europeandataportal
    european_testlink = create_modlink(link, "european")

    response = get_connection(european_testlink.format(1, 0), open_conn=True)

    if isinstance(response, requests.Response):
        link_content = get_website_data(response)
        response.close()

        if isinstance(link_content, dict):
            if "result" in link_content:
                return "european"

    # check for Socrata
    socrata_testlink = create_modlink(link, "socrata")

    response = get_connection(socrata_testlink, open_conn=True)

    if isinstance(response, requests.Response):
        link_content = get_website_data(response)
        response.close()

        if isinstance(link_content, dict):
            if "dataset" in link_content:
                return "socrata"

    return "unknown"

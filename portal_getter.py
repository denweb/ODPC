from queue import Queue
from threading import Thread

from utility.utility import get_connection
from crawler.getwebsitedata import get_website_data
from urllib3 import disable_warnings
import settings
from extractor.getdataitems import get_dataitems
import csv
import json
import requests

from portals import portals_dict

disable_warnings()

links = ["https://offenedaten.de/", "https://ckan.govdata.de/"]

portals = set()



def parse_url(url):
    """
    Parses a valid url and extract its domain.
    :param url: A valid url-string.
    :return: The extracted domain of the input String.
    """
    url = url.strip()
    if url.startswith("https"):
        url = url[8:]
    elif url.startswith("http"):
        url = url[7:]

    if url.startswith("www"):
        url = url[4:]

    url_splitted = url.split("/")

    domain = url_splitted[0]

    if any([
        not domain,
        "." not in domain,
        " " in domain
    ]):
        domain = None

    return domain


def get_providers(q):
    while not q.empty():
        dataitem = q.get()
        try:
            resource_url = dataitem["resources"][0]["url"]
            org_title = dataitem["organization"]["title"]
            domain = parse_url(resource_url)
            portals.add((org_title, domain))
        except:
            print("Keine Endpunkte oder Organisation.")

        q.task_done()


def get_portals():
    for link in links:

        # preparations
        print(link)
        # make raw API-call for meta data out of base url
        modlink = "".join([link, "api/3/action/package_search?rows={}&start={}"])

        # make test url out of raw api-url
        testlink = modlink.format(0, 1)

        # establish connection to test url
        response = get_connection(testlink, open_conn=True)

        # get needed information
        website_data = get_website_data(response)
        response.close()

        number_items_overall = website_data["result"]["count"]

        # start actual crawling
        for k in range(0, number_items_overall, settings.pagesize):
            url_current = modlink.format(settings.pagesize, k)

            # open connection to api call and retrieve data
            response = get_connection(url_current, open_conn=True)

            website_data = get_website_data(response)

            # get dataitems
            dataitems = get_dataitems(website_data, "cdkan")

            # preparations for queuing
            temp_item_number = len(dataitems)
            threads = min(settings.threads, temp_item_number)

            # initialize queue with data items
            q = Queue(maxsize=0)

            # put dataitems in the queue
            for dataitem in dataitems:
                q.put(dataitem)

            # start threads
            for i in range(threads):
                t = Thread(target=get_providers,
                           args=(q,))
                t.start()

            q.join()

            response.close()

"""
non_list = ["Braunschweig", "Open.NRW", "Rheinland-Pfalz", "Bundesministerium des Innern", "mCLOUD", "Berlin Open Data"]

for entry in portals_set:
    if entry[1] is not None:
        if entry[0] not in portals_dict:
            portals_dict[entry[0]] = [entry[1]]
        else:
            portals_dict[entry[0]].append(entry[1])
"""


def write_to_csv(test):
    with open("daten/portals.csv", "w", newline='') as file:
        f = csv.writer(file)
        f.writerow(["url", "Organisationen", "code"])

        for entry in test:
            f.writerow([
                entry["url"],
                entry["Organisationen"],
                entry["code"]
            ])
        print("CSV erfolgreich.")


portals_dict_trans = {}
for entry in portals_dict:
    for portal in portals_dict[entry]:
        if portal not in portals_dict_trans:
            portals_dict_trans[portal] = [entry]
        else:
            portals_dict_trans[portal].append(entry)
print(portals_dict_trans)

counter = 0
test = []

for entry in portals_dict_trans:
    counter += 1
    url = "".join(["http://", entry])
    response = get_connection(url)
    if isinstance(response, requests.Response):
        code = response.status_code
    else:
        url = "".join(["http://www.", entry])
        response = get_connection(url)
        if isinstance(response, requests.Response):
            code = response.status_code
        else:
            code = "error"
    test.append({"url": entry, "Organisationen": portals_dict_trans[entry], "code": code})
    print(counter, url, code)

print(test)

write_to_csv(test)

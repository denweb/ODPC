import csv
from urllib3 import disable_warnings
from utility.deceider import get_link_portal
from transformer.helper.getdomain import get_domain
from queue import Queue
from utility.utility import get_connection
from threading import Thread
from requests import Response


def link_gen(url):
    heads = ["http://", "https://", "http://www.", "https://www."]

    for head in heads:
        gen_url = "".join([head, url])
        if check_code(gen_url):
            return gen_url


def check_code(url):
    resp = get_connection(url)
    if isinstance(resp, Response):
        return resp.status_code == 200
    else:
        return False


def get_portal(q):
    while not q.empty():

        global counter
        counter += 1

        url_infos = q.get()

        testlink = link_gen(url_infos)

        # test given url
        if testlink not in seen_urls:
            link, portal = get_link_portal(testlink)

            seen_urls.add(link)

            results.add((link, portal))

            print(url_infos, link, portal, "".join([str(counter), "/", number_urls]))

        q.task_done()


# declare variables
disable_warnings()
results = set()
seen_urls = set()
counter = 0

# read url infos from file
with open("daten/portals.csv", newline='') as file:
    reader = csv.reader(file, delimiter=";")
    url_test = [row[0].strip() for row in reader]

url_test.pop(0)
number_urls = str(len(url_test))

# put url infos into queue
q = Queue(maxsize=0)

for url_infos in url_test:
    q.put(url_infos)

# start threads with queue
for i in range(50):
    t = Thread(target=get_portal,
               args=(q,))
    t.start()

q.join()

# write results to file
with open("daten/portals_checked.csv", "w", newline='') as csvout:
    writer = csv.writer(csvout, delimiter=";", quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["URL", "Portal"])

    for result in results:
        writer.writerow([result[0], result[1]])


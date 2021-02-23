import logging
from datetime import datetime
from urllib3 import disable_warnings
from utility.utility import set_limit_and_offset
from crawlers.crawler import Crawler
from utility.deceider import assign
import sys

if __name__ == '__main__':

    # initialise logging
    timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    logging.basicConfig(filename="logs/%s.log" % timestamp,
                        level=logging.INFO,
                        format="%(asctime)s:%(levelname)s:%(message)s")
    logging.info("Crawler started")

    disable_warnings()

    # check if a download-limit or an offset is given and set the variables accordingly. No specification = 0
    if len(sys.argv) < 2:
        download_limit = 0
        offset = 0
    else:
        download_limit, offset = set_limit_and_offset(sys.argv)

    logging.info("Crawler limit set to: %s and offset set to: %s" % (download_limit, offset))

    # get URLS to crawl
    with open("links.txt") as f:
        url_test = f.readlines()

    url_test = set([x.strip() for x in url_test])

    logging.info("{} links extracted from links.txt".format(len(url_test)))

    for link in url_test:
        logging.info("Processing link: {}".format(link))

        portal = assign(link)
        logging.info("Detected portal: {}".format(portal))

        c = Crawler(link, portal, download_limit, offset)

        c.crawl()

        logging.info("New IDs: %s" % c.uploaded_ids)
        logging.info("%s Dataitems seen on this link" % c.number_items)
        logging.info("%s Dataitems loaded of this link" % len(c.uploaded_ids))
        logging.info("\n")
    logging.info("Crawler done")

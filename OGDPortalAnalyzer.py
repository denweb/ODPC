import logging
from datetime import datetime
from urllib3 import disable_warnings
from utility.utility import set_limit_and_offset
from crawlers.crawler import Crawler
from rawDataValidation import validate_raw_data_links
from qualityAnalyzer import analyze
import sys
import csv

if __name__ == '__main__':
    """
    Führt eine komplette Analyse auf die in der 'portale_gesamt_sortiert.csv' enthaltenen Portale aus
    und speichert die Ergebnisse wie in der Arbeit beschrieben in den Datenbanken.
    """

    timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    logging.basicConfig(filename="logs/%s.log" % timestamp,
                        level=logging.INFO,
                        format="%(asctime)s:%(levelname)s:%(message)s")
    logging.info("Open Data Portal Crawler started")

    disable_warnings()

    if len(sys.argv) < 2:
        download_limit = 0
        offset = 0
    else:
        download_limit, offset = set_limit_and_offset(sys.argv)

    logging.info("Crawler limit set to: %s and offset set to: %s" % (download_limit, offset))

    # get URLS to crawl
    with open("portale_gesamt_sortiert.csv", "r") as f:
        reader = csv.DictReader(f)
        portals_info = list(reader)

    logging.info("{} portals extracted from portal list".format(len(portals_info)))
    i = 0

    # Führt für jedes Portal in der angegebenen CSV Datei den Crawl Vorgang in die DB durch.
    for portal in portals_info:
        logging.info("Processing link: {}".format(portal["URL"]))
        i += 1
        print(i)

        c = Crawler(portal, download_limit, offset)

        c.crawl()

        logging.info("%s Dataitems seen on this link" % c.number_items)
        logging.info("%s Dataitems loaded of this link" % len(c.uploaded_ids))
        logging.info("\n")
    logging.info("Crawler done")

    # Validiert alle Rohdaten-Links in der Datenbank
    logging.info("Starting raw data validation")
    validate_raw_data_links()
    logging.info("Raw data validation done.")

    logging.info("Starting Framework Analysis")

    # Untersucht alle bisher ermittelten Daten mithilfe des DQ Frameworks
    # und speichert die Ergebnisse in der Frameowk.db
    analyze()

    logging.info("Framework Analysis done.")




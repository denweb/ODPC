from crawler.getwebsitedata import get_website_data
from utility.utility import get_connection, create_modlink
from extractor.getdataitems import get_dataitems
from loader.loader import upload
from transformer.european.transformation import remap as euro_remap
from transformer.ckan.transformation import remap as ckan_remap
from transformer.arcgis.transformation import remap as arcgis_remap
from transformer.socrata.transformation import remap as socrata_remap
from utility.websiteInfo import check_all
import settings
import requests
from queue import Queue
from threading import Thread
import logging
import json


class Crawler (object):
    def __init__(self, link, portal, limit, offset):
        self.link = link
        self.portal = portal
        self.modlink = create_modlink(link, portal)
        self.limit = limit
        self.offset = offset
        self.uploaded_ids = []
        self.number_items = 0
        self.number_items_overall = 0
        self.pagesize = settings.pagesize
        self.threads = settings.threads

    def get_website_data(self, response):

        website_data = get_website_data(response)

        response.close()

        return website_data

    def get_dataitems(self, website_data):
        dataitems = get_dataitems(website_data, self.portal)

        return dataitems

    def upload_item(self, dataitem):
        statuscode, id = upload(dataitem)

        return statuscode, id

    def crawl(self):
        if self.initial_check():
            logging.info("Initial check passed.")
            logging.info("Total number of data items on this link: {}".format(self.number_items_overall))

            # portal decides in which way to paginate through the site.
            if self.portal == "european":
                if self.limit == 0:
                    self.limit = self.number_items_overall

                for k in range(self.offset, self.limit, self.pagesize):
                    url_current = self.modlink.format(self.pagesize, k)

                    self.extract_and_process_website(url_current)

            elif self.portal == "ckan":
                if self.limit == 0:
                    self.limit = self.number_items_overall

                for k in range(self.offset, self.limit, self.pagesize):
                    url_current = self.modlink.format(self.pagesize, k)

                    self.extract_and_process_website(url_current)

            elif self.portal == "dkan":
                self.extract_and_process_website(self.modlink)
                # Todo: Rest für DKAN eintragen

            elif self.portal == "opendatasoft":
                self.extract_and_process_website(self.modlink)
                # Todo: Rest für opendatasoft eintragen

            elif self.portal in ["socrata", "arcgis"]:
                self.extract_and_process_website(self.modlink)
        else:
            logging.info("Initial check not passed for {}".format(self.link))

    def initial_check(self):
        """
        Checks if the crawled website is online and has data items.
        :return: Boolean True or False
        """
        proceed = False

        # get test-url for minimum call
        if self.portal in ["ckan", "european"]:
            modlink = self.modlink.format(1, 0)
        else:
            modlink = self.modlink

        # check if url is still available
        response = get_connection(modlink, open_conn=True)
        if isinstance(response, requests.Response):

            url_info = check_all(response)

            if url_info["url_status"] == "200, OK":
                website_data = get_website_data(response)
                response.close()

                if website_data is not None:
                    if self.portal in ["ckan", "european"]:
                        self.number_items_overall = website_data["result"]["count"]
                    else:
                        self.number_items_overall = len(website_data['dataset'])

                if self.number_items_overall > 0:
                    proceed = True
                else:
                    logging.info("No data items on this website.")

        return proceed

    def extract_and_process_website(self, url_current):
        logging.info("Extraction for url {}".format(url_current))

        # get the actual data
        response = get_connection(url_current, open_conn=True)
        if isinstance(response, requests.Response):

            website_data = self.get_website_data(response)

            if website_data is not None:
                logging.info("Transformation & Loading started.")
                self.process_website_data(website_data)

                logging.info("Transformation & Loading finished. %s items uploaded" % len(self.uploaded_ids))
                logging.info("Number of items seen so far: %s" % self.number_items)
            else:
                logging.info("No JSON on {}".format(url_current))

        else:
            logging.info("Connection failed to {}".format(url_current))

    def process_website_data(self, website_data):
        dataitems = self.get_dataitems(website_data)

        # transforming and loading
        temp_item_number = len(dataitems)
        self.threads = min(self.threads, temp_item_number)

        q = self.put_dataitems_in_queue(dataitems)

        self.start_threads(q)

        q.join()

        self.number_items += temp_item_number

    def put_dataitems_in_queue(self, dataitems):
        q = Queue(maxsize=0)

        # put dataitems in the queue
        for dataitem in dataitems:
            q.put(dataitem)

        return q

    def start_threads(self, q):
        for i in range(self.threads):
            t = Thread(target=self.transform_and_upload,
                       args=(q,))
            t.start()

    def transform_and_upload(self, q):
        while not q.empty():
            dataitem = q.get()

            if self.portal == "european":
                remapped = euro_remap(dataitem)
            elif self.portal == "ckan":
                remapped = ckan_remap(dataitem)
            elif self.portal == "arcgis":
                remapped = arcgis_remap(dataitem)
            elif self.portal == "socrata":
                remapped = socrata_remap(dataitem)
            else:
                remapped = None

            logging.debug("Remapping done")

            # checks if the transformation was successfull. Otherwise skips the rest

            if remapped is not None:

                if settings.upload:

                    # loading
                    logging.debug("Loading for %s" % remapped["uuid"])

                    # loads the transformed dataitem into the DB
                    status_code, id = upload(remapped)

                    # checks if the upload was successfull. if write, give the dataitem and the status_code in the log file
                    if status_code == 200:
                        logging.debug("Sucessfully uploaded dataitem. New ID = %s" % id)
                        self.uploaded_ids.append(id)

                    elif type(status_code) is not int:
                        logging.warning(status_code)

                    else:
                        logging.warning(
                            "Could not upload dataitem %s. Status code: %s\n%s" % (
                                remapped['uuid'], status_code, json.dumps(remapped)))

            else:
                logging.debug("Not a valid dataitem")

            q.task_done()

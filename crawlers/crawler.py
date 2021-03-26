from crawler.getwebsitedata import get_website_data
from utility.utility import get_connection, create_modlink
from extractor.getdataitems import get_dataitems
from loader.loader import upload
from transformer.european.transformation import remap as euro_remap
from transformer.cdkan.transformation import remap as ckan_remap
from transformer.arcgis.transformation import remap as arcgis_remap
from transformer.socrata.transformation import remap as socrata_remap
from utility.websiteInfo import check_all
import settings
import requests
from queue import Queue
from threading import Thread
import logging
from utility.deceider import get_link_portal


class Crawler (object):
    def __init__(self, portal, limit, offset):
        self.portal_info = portal
        self.orig_link = portal["URL"]
        self.link = ""
        self.portal_id = None
        self.portal_type = None
        self.modlink = None
        self.limit = limit
        self.offset = offset
        self.uploaded_ids = []
        self.number_items = 0
        self.number_items_overall = 0
        self.pagesize = settings.pagesize
        self.threads = settings.threads

    def crawl(self):

        # Initiating necessary variables
        self.link, self.portal_type = get_link_portal(self.orig_link)
        logging.info("For {0} detected portal: {1}".format(self.link, self.portal_type))

        self.modlink = create_modlink(self.link, self.portal_type)

        # Upload portal data before processing items to gain portal ID
        self.portal_id = self.upload_portal()

        # check for known portal type and availability of website
        if self.portal_type in ["cdkan", "dkan", "arcgis"]:
            if self.initial_check():
                logging.info("Initial check passed.")
                logging.info("Total number of data items on this link: {}".format(self.number_items_overall))

                # portal decides in which way to paginate through the site.
                if self.portal_type == "european":
                    if self.limit == 0:
                        self.limit = self.number_items_overall

                    for k in range(self.offset, self.limit, self.pagesize):
                        url_current = self.modlink.format(self.pagesize, k)

                        self.extract_and_process_website(url_current)

                elif self.portal_type == "cdkan":
                    if self.limit == 0:
                        self.limit = self.number_items_overall

                    for k in range(self.offset, self.limit, self.pagesize):
                        url_current = self.modlink.format(self.pagesize, k)

                        self.extract_and_process_website(url_current)

                elif self.portal_type == "dkan":
                    self.extract_and_process_website(self.modlink)

                elif self.portal_type == "opendatasoft":
                    url_current = self.modlink.format(self.number_items_overall)

                    self.extract_and_process_website(url_current)

                elif self.portal_type in ["socrata", "arcgis"]:
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
        if self.portal_type in ["cdkan", "european"]:
            modlink = self.modlink.format(1, 0)
        elif self.portal_type == "opendatasoft":
            modlink = self.modlink.format(1)
        else:
            modlink = self.modlink

        # check if url is still available
        response = get_connection(modlink, open_conn=True)
        if isinstance(response, requests.Response):

            url_info = check_all(response)

            if url_info["url_status"] == "200, OK":
                website_data = get_website_data(response)
                response.close()

                # Number of items overall is needed for the correct API call for some portals later.
                if website_data is not None:
                    if self.portal_type in ["cdkan", "european"]:
                        self.number_items_overall = website_data["result"]["count"]
                    elif self.portal_type in ["socrata", "arcgis"]:
                        self.number_items_overall = len(website_data['dataset'])
                    elif self.portal_type == "dkan":
                        self.number_items_overall = len(website_data["result"][0])
                    elif self.portal_type == "opendatasoft":
                        self.number_items_overall = website_data["total_count"]
                
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

            website_data = get_website_data(response)
            response.close()

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
        dataitems = get_dataitems(website_data, self.portal_type)

        # transforming and loading
        temp_item_number = len(dataitems)
        self.threads = min(self.threads, temp_item_number)

        q = self.put_dataitems_in_queue(dataitems)

        self.start_threads(q,)

        q.join()

        self.number_items += temp_item_number

    @staticmethod
    def put_dataitems_in_queue(dataitems):
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

            if self.portal_type == "european":
                remapped = euro_remap(dataitem, self.portal_id)
            elif self.portal_type in ["cdkan", "dkan"]:
                remapped = ckan_remap(dataitem, self.portal_id)
            elif self.portal_type == "arcgis":
                remapped = arcgis_remap(dataitem, self.portal_id)
            elif self.portal_type == "socrata":
                remapped = socrata_remap(dataitem, self.portal_id)
            else:
                remapped = None

            # print(remapped)

            logging.debug("Remapping done")

            # checks if the transformation was successfull. Otherwise skips the rest

            if remapped is not None:

                if settings.upload:
                    # Todo: get results for each data item and add to DB.

                    upload(remapped, "meta")

            else:
                logging.debug("Not a valid dataitem")

            q.task_done()

    def upload_portal(self):

        portal_data = {
            "titel": self.portal_info["Titel"],
            "url": self.link,
            "notizen": self.portal_info["Notizen"],
            "portalTyp": self.portal_type,
            "betreiber": None,
            "betreiberTyp": None,
            "elternInstanz": None
        }

        return upload(portal_data, "portal")

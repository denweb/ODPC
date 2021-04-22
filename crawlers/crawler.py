from crawler.getwebsitedata import get_website_data
from utility.utility import get_connection, create_modlink
from extractor.getdataitems import get_dataitems
from loader.loader import upload
from transformer.cdkan.transformation import remap as ckan_remap
from transformer.arcgis.transformation import remap as arcgis_remap
from utility.websiteInfo import check_all
import settings
import requests
from queue import Queue
from threading import Thread
import logging
from utility.deceider import get_link_portal


class Crawler (object):
    """
    Beinhaltet den kompletten Crawl-Prozess für den Datenbestand eines Datenportals.
    Aus einer alten Arbeit übernommen. Die anderen Teile sollten in Zukunft ähnlich aufgebaut werden.
    """

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
        """
        Initiiert den Crawl-Prozess für den Datenbestand eines OGD-Portals in die DB.
        Überprüft in diesem Schritt, ob es sich um eine Portalsoftware handelt und ob Datensätze vorhanden sind.
        """
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

                # Aktuell nicht genutzt
                if self.portal_type == "european":
                    if self.limit == 0:
                        self.limit = self.number_items_overall

                    for k in range(self.offset, self.limit, self.pagesize):
                        url_current = self.modlink.format(self.pagesize, k)

                        self.extract_and_process_website(url_current)

                # CKAN und DKAN gleich behandeln, da sie das gleiche Metadatenschema nutzen.
                elif self.portal_type == "cdkan":
                    if self.limit == 0:
                        self.limit = self.number_items_overall

                    for k in range(self.offset, self.limit, self.pagesize):
                        url_current = self.modlink.format(self.pagesize, k)

                        self.extract_and_process_website(url_current)

                elif self.portal_type == "dkan":
                    self.extract_and_process_website(self.modlink)

                # Aktuell nicht verfügbar
                elif self.portal_type == "opendatasoft":
                    url_current = self.modlink.format(self.number_items_overall)

                    self.extract_and_process_website(url_current)

                elif self.portal_type in ["socrata", "arcgis"]:
                    self.extract_and_process_website(self.modlink)
            else:
                logging.info("Initial check not passed for {}".format(self.link))

    def initial_check(self):
        """
        Überprüft, ob ein OGD-Portal erreichbar ist und Datensätzesätze enthält.
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
        """
        Extrahiert den die Datensätze eines OGD-Portals und übergibt sie an die Transformation.
        :param url_current: URL des OGD-Portals
        """
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
        """
        Initiiert Threads für den Transformationsprozess der einzelnen Datensätze
        :param website_data: Extrahiert Datensätze eines OGD-Portals
        """
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
        """
        Lädt die Datensätze für die Verarbeitung in den Threads in eine Queue.
        :param dataitems: Extrahierte Datensätze eines OGD-Portals.
        :return: Eine Queue mit den Datensätzen.
        """
        q = Queue(maxsize=0)

        # put dataitems in the queue
        for dataitem in dataitems:
            q.put(dataitem)

        return q

    def start_threads(self, q):
        """
        Startet die Threads, welche die Datensätze in der Queue transformieren.
        :param q: Eine Queue mit den extrahierten Datensätzen
        """
        for i in range(self.threads):
            t = Thread(target=self.transform_and_upload,
                       args=(q,))
            t.start()

    def transform_and_upload(self, q):
        """
        Funtkion eines Threads, die den einen Datensatz aus der Q nimmt, diesen entsprechend des Portalsoftwaretypens
        transformiert und das Ergebnis in die DB lädt.
        :param q: Eine Queue mit den extrahierten Datensätzen
        """
        while not q.empty():
            dataitem = q.get()

            if self.portal_type == "european":
                pass
            elif self.portal_type in ["cdkan", "dkan"]:
                remapped = ckan_remap(dataitem, self.portal_id)
            elif self.portal_type == "arcgis":
                remapped = arcgis_remap(dataitem, self.portal_id)
            elif self.portal_type == "socrata":
                pass
            else:
                remapped = None

            logging.debug("Remapping done")

            # checks if the transformation was successfull. Otherwise skips the rest
            if remapped is not None:

                if settings.upload:

                    upload(remapped, "meta")

            else:
                logging.debug("Not a valid dataitem")

            q.task_done()

    def upload_portal(self):
        """
        Lädt die grundlegenden Infos zum OGD-Portal in die DB.
        :return: Statuscode des Uploadergebnisses.
        """
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

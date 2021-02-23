import re
import requests
import json
import logging
from os import listdir
from datetime import datetime
from threading import Thread
from queue import Queue
from urllib3 import disable_warnings
from utility.websiteInfo import check_all


def get_file_info(url):
    """
    Calls the "check_all"-function to return a dictionary with information about status_code, size, mimetype and
    possoble extension of given url-response-object
    :param url: a HTTP response-object to check
    :return: a dictionary with the crawled information
    """

    return check_all(url)


def get_filename(response, url, ext):
    """
    Creates a filename for the file to be downloaded. Checks for header-info, url-path or else generates a dummy-one.
    :param response: the response object of the called download-url for the header-info
    :param url: the url itself for parsing
    :param ext: the file extension
    :return: a string containing the generated filename
    """

    # try content-disposition in header
    cd = response.headers.get('content-disposition')
    if cd is not None:
        filename = re.findall('filename=(.+)', cd)
        if filename:
            return filename[0]

    # try to parse url for filename
    url_ending = url.split("/")[-1]
    if "." in url_ending:
        return "".join([url_ending.split(".")[0], ".", ext])

    # if all above fails: return a dummy filename with the corresponding extension
    return "".join(["datafile", ".", ext])


def download_file(q, files_generated):
    """
    Downloads the file from a given URL, which are stored in a queue-object and saves it in the "output"-folder.
    :param q: a queue-object, which contains pairs of URLs for dataendpoints with the corresponding name of the data-
    item it belongs to.
    :param files_generated: a list to store the generated filenames in
    """

    while not q.empty():
        linkdata = q.get()
        url = linkdata[1]
        title = linkdata[0]

        try:
            with requests.get(url, verify=False, stream=True, timeout=20) as response:

                # check for status code and mimetype
                file_info = get_file_info(response)

                # check if url is reachable and mimetype is viable
                if file_info["url_status"] == "200, OK":
                    if file_info["ext"] is not None:
                        if any(["CSV" in file_info["ext"],
                                "JSON" in file_info["ext"],
                                "XLS" in file_info["ext"],
                                "XLSX" in file_info["ext"],
                                "EXCEL" in file_info["ext"],
                                "KML" in file_info["ext"]]):

                            downloadlogger.info("Downloading %s (%s)" % (url, response.headers.get("content-length")))

                            # generate filename
                            filename = get_filename(response, url, file_info["ext"].lower())

                            # check if filename = title to avoid redundancy
                            if filename.replace("_", " ").split(".")[0].lower() == title.lower():
                                output_filename = filename
                            else:
                                output_filename = "".join([title, "_", filename])

                            # save the file
                            with open("".join(["output/", output_filename]), "wb") as f:
                                f.write(response.content)

                            files_generated.append(output_filename)

                            downloadlogger.debug("Finished Processing: %s\nCreated file: %s" % (url, output_filename))

                        else:
                            downloadlogger.debug("Wrong data type for: %s Parsed: %s" % (url, file_info["ext"]))
                    else:
                        downloadlogger.debug("Not extension can be extracted for: %s" % url)
                else:
                    downloadlogger.debug("URL no reachable: %s" % url)
        except:
            downloadlogger.warning("Uncaught Error while processing URL: %s" % url)

        q.task_done()


if __name__ == '__main__':
    # initialise logging
    timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    logfile = "logs/downloader-%s.log" % timestamp
    loglevel = logging.INFO
    logformat = "%(asctime)s:%(levelname)s:%(message)s"

    downloadlogger = logging.getLogger("downloadlogger")
    downloadlogger.setLevel(loglevel)
    downloadlogger_filehander = logging.FileHandler(logfile)
    downloadlogger_filehander.setLevel(loglevel)
    downloadlogger_filehander.setFormatter(logging.Formatter(logformat))
    downloadlogger.addHandler(downloadlogger_filehander)

    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    downloadlogger.info("Downloader started")

    # disable ssl-warnings
    disable_warnings()

    # helping variables
    files_generated_total = []
    number_links_total = 0

    for file in listdir("../output/datalists"):
        # load the data from json
        with open("".join(["../output/datalists/", file])) as f:
            url_test = json.load(f)

        downloadlogger.info("Processing Portal: %s" % file)

        files_generated = []
        number_links_portal = len(url_test)
        number_links_total += number_links_portal

        # number of threads to run
        num_threads = min(len(url_test), 20)

        q = Queue(maxsize=0)

        for url in url_test:
            q.put((url[0], url[1].strip()))

        for i in range(num_threads):
            t = Thread(target=download_file, args=(q, files_generated,))
            t.start()

        q.join()

        files_generated_total.extend(files_generated)

        downloadlogger.info("Finished processing file: %s" % file)
        downloadlogger.info("%s links processed. %s files downloaded." % (number_links_portal, len(files_generated)))

    downloadlogger.info("Downloader finished")
    downloadlogger.info(
        "%s links processed in total. %s files downloaded" % (number_links_total, len(files_generated_total)))
    downloadlogger.info("Files downloaded: %s" % files_generated_total)

from database.dbcon import DBConnection
import requests
import os
from queue import Queue
from threading import Thread
from utility.utility import get_connection
from utility.websiteInfo import check_all
import re
from linting.lintData import get_valid
import urllib3


def get_links():
    db = DBConnection()
    res = [{"id": entry[0], "link": entry[1]} for entry in db.get_rawdata_links()]

    db.connection.close()

    return res


# Todo: Evtl. Connection in Thread-Funktion legen?
def update_dataitem(id, res):
    db = DBConnection()

    res = db.update_rawdata(id, res)

    db.connection.commit()
    db.connection.close()

    return res


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


def validate_link(q):
    while not q.empty():
        link_info = q.get()
        link = link_info["link"]
        lid = link_info["id"]

        response = get_connection(link, open_conn=True)

        if isinstance(response, requests.Response):

            url_info = check_all(response)

            if url_info["url_status"] == "200, OK":
                # Todo: Herausfinden, welche files genau geparsed werden könne. Was ist mit XML? XSL?
                # Todo: Add support for archives like zip, tar or rar. Could be done with shutil
                online = True
                ext = url_info["ext"]
                if ext in ["CSV",
                            "XLS",
                            "JSON",
                            "GEOJSON"]:

                    # Damit GEOJSON Dateien wenigstens auf JSON validität geparsed werden.
                    if ext != "GEOJSON":
                        filename = get_filename(response, link, ext)
                    else:
                        filename = get_filename(response, link, "JSON")

                    filepath = "".join(["rawdata/", filename])
                    print(filename, filepath)

                    try:
                        with open(filepath, "wb") as f:
                            f.write(response.content)
                        if os.path.isfile(filepath):
                            try:
                                validation = get_valid(filepath)

                                # Todo: Add information about file to result
                                # merke tatsächliche Dateigröße
                                actual_size = os.path.getsize(filepath)
                                validation["dateiGrößeReal"] = actual_size

                                update = update_dataitem(lid, validation)

                                print(update)
                            except Exception as e:
                                print("Validation Error", e)

                            os.remove(filepath)
                        else:
                            print("Save file not created successfully // Could not be read")
                    except:
                        print("Error. Save to ID or something")
                else:
                    # print("Save not supported file type", ext)
                    pass

            response.close()
        q.task_done()


# Todo: Testen auf Server mit großer Menge, ob Fehler gefunden / upgedated werden.
urllib3.disable_warnings()

links = get_links()[100:150]
q = Queue(maxsize=0)

for link in links:
    q.put(link)

for i in range(3):
    t = Thread(target=validate_link, args=(q, ))
    t.start()

q.join()

# put links in list (csv?) for better control in case of error
# put links in q ?

# res = update_dataitem(1, "Yo")
# res = get_links()

# print(res)

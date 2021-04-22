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
    """
    Extrahiert alle Rohdatenlinks aus allen Metadaten, die in der Daten-DB enthalten sind.
    :return: Die extrahierten Rohdatenlinks in einer Liste
    """
    db = DBConnection("testdb.db")
    res = [{"id": entry[0], "link": entry[1]} for entry in db.get_rawdata_links()]

    db.connection.close()

    return res


# Todo: Evtl. Connection in Thread-Funktion legen?
def update_dataitem(id, res):
    """
    Updated den Datenbankeintrag eines Rohdatensatzes (mit den Validierungsergebnissen)
    :param id: ID des Rohdatensatzes (Int)
    :param res: Standardisierte Validierungsergebnisse (Dictionary)
    :return: ID des geupdateten Eintrags (Int)
    """
    db = DBConnection("testdb.db")

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
    """
    Arbeitet eine Queue mit Rohdatenlinks ab. Überprüft ob ein Links online ist und ob eine Rohdatendatei ermittelt
    werden kann. Ist dies der Fall und hat die Datei einen validen Dateityp, kann sie heruntergeladen
    validiert werden. Anschließend werden alle gesammelten Ergebnisse in die Daten-DB geladen.
    :param q: Eine Queue mit den Rohdatenlinks
    """
    while not q.empty():
        link_info = q.get()
        link = link_info["link"]
        lid = link_info["id"]

        # To save all generated new information
        updated_data_item = {
            "online": False,
            "dateiTypReal": None,
            "dateiGrößeReal": None,
            "valide": 2,
            "fehler": None,
            "anzahlFehler": None,
        }

        response = get_connection(link, open_conn=True)

        if isinstance(response, requests.Response):

            url_info = check_all(response)

            if url_info["url_status"] == "200, OK":
                # Todo: Add support for archives like zip, tar or rar. Could be done with shutil
                ext = url_info["ext"]

                updated_data_item["online"] = True
                updated_data_item["dateiTypReal"] = ext

                if ext in ["CSV",
                            "XLS",
                            "XLSX",
                            "ODS",
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
                                # merke tatsächliche Dateigröße
                                actual_size = os.path.getsize(filepath)
                                updated_data_item["dateiGrößeReal"] = actual_size

                                # Validation
                                validation = get_valid(filepath)
                                updated_data_item["valide"] = validation["valide"]
                                updated_data_item["fehler"] = validation["fehler"]
                                updated_data_item["anzahlFehler"] = validation["anzahlFehler"]

                            except Exception as e:
                                print("Validation Error", e)

                            os.remove(filepath)
                        else:
                            updated_data_item["valide"] = 4
                            print("Save file not created successfully // Could not be read")
                    except Exception:
                        updated_data_item["valide"] = 5
                        print("Error. Save to ID or something")
                else:
                    # print("Save not supported file type", ext)
                    pass

            response.close()

        # Quckfix f. Fehler bei der Fehlererstellung. Todo: später genauer untersuchen.
        try:
            update_dataitem(lid, updated_data_item)
        except Exception as e:
            print("Fehler beim updaten:", e)
        q.task_done()


def validate_raw_data_links():
    """
    Initiiert die Überprüfung und Validierung aller Rohdatenlinks in der Daten-DB.
    Extrahiert dazu die Links und verarbeitet diese parallel in Threads.
    """
    urllib3.disable_warnings()

    links = get_links()
    q = Queue(maxsize=0)

    for link in links:
        q.put(link)

    for i in range(3):
        t = Thread(target=validate_link, args=(q, ))
        t.start()

    q.join()

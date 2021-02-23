import http
import http.client
import mimetypes
import sys
import urllib.request
import urllib.parse
import urllib.error
from socket import timeout


def get_extension(response):
    """
    Checks for the MIME-Type and the extension (if possible) of any given URL.
    :param response: URL of the website to be checked.
    :return: Detected MIME-Type and extension of given URL or error-message
    """

    content_type = response.headers.get('content-type')

    if content_type is None:
        content_type = "unknown"
    elif ";" in content_type:
        csplit = content_type.split(";")
        content_type = csplit[0]

    try:
        ext = mimetypes.guess_extension(content_type)
    except AttributeError:
        ext = None

    # extract the extension, if the mimetypes-library returns "None"
    try:
        if "stream" in content_type:
            ext = response.url.split(".")[-1]
        elif all([ext is None, content_type != "unknown"]):
            ext = content_type.split(";")[0].split("/")[1]
        elif ext is not None:
            ext = ext[1:]
        elif ext is None:
            ext = content_type
    except IndexError:
        ext = content_type

    # check for special cases
    if ext == "pyz":
        ext = "zip"
    elif ext == "htm":
        ext = "html"
    elif ext == "turtle":
        ext = "ttl"
    elif ext == "VND.GOOGLE-EARTH.KML+XML":
        ext = "kml"
    elif ext == "xlb":
        ext = "xls"
    elif ext == "geo+json":
        ext = "geojson"

    return content_type.upper(), ext.upper()


def check_url(response):
    """
    Checks the online-status of a given URL.
    :param response: URL of the website to be checked.
    :return: Availability of the given URL and the status-code (if possible)
    """

    code = response.status_code

    if code == 200:
        return "200, OK"
        # dont do further checks for now because of read() slowing things down.
        """
        #check if response is decodeable (html / some kind of text-file)
        try:
            html_low = response.read().decode().lower()

            #check for keywords in page
            if not any(["page not found" in html_low, "not found" in html_low, "could not be found" in html_low,
                        "failed to find response" in html_low]):
                return "200, OK"
            else:
                return "404, not found"
        except ValueError:
            return "200, OK"
        except http.client.IncompleteRead:
            return "404, not found"
        """
    else:
        return "%s, Site not available" % code


def get_size(response):
    """
    Returns the filesize of the website/object of the given URL.
    :param response: URL of the website to be checked
    :return: The filesize of the given URL
    """

    size = response.headers.get('content-length')

    # only read the object, if the filesize is not given in the header information
    if size is None:
        # size = sys.getsizeof(response.read())
        return 0

    size_normalized = int(round(((int(size)/1024)/1024)))

    if size_normalized == 0:
        size_normalized = 1

    return size_normalized


def check_all(response):

    try:
        url_status = check_url(response)
        if url_status == "200, OK":
            mimetype, ext = get_extension(response)
            size = get_size(response)
        else:
            mimetype = None
            ext = None
            size = None

    except urllib.error.HTTPError as e:
        url_status = "%s, %s" % (e.code, e.reason)
        mimetype = None
        ext = None
        size = None
    except urllib.error.URLError as e:
        url_status = "%s" % e.reason
        mimetype = None
        ext = None
        size = None
    except ConnectionError as e:
        url_status = "%s" % e
        mimetype = None
        ext = None
        size = None
    except ValueError as e:
        url_status = "%s, Not a valid URL" % e
        mimetype = None
        ext = None
        size = None
    except timeout:
        url_status = "Not a valid URL"
        mimetype = None
        ext = None
        size = None
    except TimeoutError as e:
        url_status = "%s" % e
        mimetype = None
        ext = None
        size = None
    except http.client.InvalidURL:
        url_status = "Not a valid URL"
        mimetype = None
        ext = None
        size = None
    except http.client.BadStatusLine:
        url_status = "Not a valid URL"
        mimetype = None
        ext = None
        size = None
    except:
        url_status = "Not a valid URL"
        mimetype = None
        ext = None
        size = None

    return {"url_status": url_status, "mimetype": mimetype, "ext": ext, "size": size}

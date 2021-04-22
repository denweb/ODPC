import dateparser
import datetime


def transform_date(date, portal=None):
    """
    Standardisiert Daten-Strings der einzelnen Portalsoftwaretypen
    :param date: Das zu standardisierende Datum (String)
    :param portal: Der Portalsoftwaretyp (String)
    :return: Der standardisierte Datenstring
    """
    res = None

    if date:
        try:
            if portal in ["european", "cdkan", "dkan"]:
                res = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d")
            elif portal == "arcgis":
                res = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
            else:
                res = datetime.datetime.strptime(date[:-3], "%Y-%m-%dT%H:%M:%S+%f").strftime("%Y-%m-%d")
        except Exception:
            date = date.split()[-1]
            try:
                res = dateparser.parse(date).strftime("%Y-%m-%d")
            except Exception:
                pass

    return res

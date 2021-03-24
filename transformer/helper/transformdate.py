import dateparser
import datetime


# Todo: Anderes Datenformat
def transform_date(date, portal=None):
    res = None

    if date:
        try:
            if portal in ["european", "ckan", "dkan"]:
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

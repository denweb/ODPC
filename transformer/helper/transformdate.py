import dateparser
import datetime


# Todo: Anderes Datenformat
def transform_date(date, portal=None):
    res = None

    if date:
        try:
            if portal in ["european", "ckan", "dkan"]:
                res = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+"+0000"
            elif portal == "arcgis":
                res = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "+0000"
            else:
                res = datetime.datetime.strptime(date[:-3], "%Y-%m-%dT%H:%M:%S+%f").strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "+0000"
        except:
            date = date.split()[-1]
            res = dateparser.parse(date).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+"+0000"

    return res
def transform_garbage(garbage, portal):
    """
    Transformiert noch nicht verwendete Daten in einen einzelnen String.
    :param garbage: Eine Liste der noch nicht genutzten Daten (List)
    :param portal: Portalsoftwaretyp (String)
    :return: Ein standardisierter String der nicht genutzten Daten.
    """
    if portal in ["european", "cdkan", "dkan"]:
        result = [
            str(item["value"]) for item in garbage
        ]
    elif portal in ["arcgis", "socrata"]:
        result = [
            str(garbage[item]) for item in garbage
        ]
    else:
        result = []

    return str(result)

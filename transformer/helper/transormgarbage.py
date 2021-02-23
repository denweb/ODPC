def transform_garbage(garbage, portal):
    if portal in ["european", "ckan", "dkan"]:
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

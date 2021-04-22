def transform_keywords(keywords, portal):
    """
    Transformiert die Tags eines Datensatzes in ein standardisiertes Format.
    :param keywords: Die Tag-Daten wie im Datensatz angegeben (List)
    :param portal: Der Portalsoftwaretyp (String)
    :return: Eine Liste mit den extrahierten und standardisierten Tags
    """
    if keywords is not None:

        if portal in ["european", "cdkan"]:

            result = [keyword["name"].upper() for keyword in keywords
                      if any([len(keyword["name"]) >= 1, len(keyword["name"]) < 100])]

        elif portal in ["arcgis", "socrata"]:

            result = [keyword.upper() for keyword in keywords
                      if all([len(keyword) > 1, len(keyword) < 100])]
        else:
            result = []
    else:
        result = []

    return result

def transform_keywords(keywords, portal):
    if keywords is not None:

        if portal in ["european", "ckan"]:

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

from json import load


def get_categorie_mapping():
    """
    reads the termmapping.json and remaps it to a dictionary so that each keyword is a key with its corresponding
    categories as values
    :return: a dictionary with each keyword as a key and its corresponding categorie as the value(s)
    """

    categorie_mappings = {}

    for entry in mapping_categories["termmappings"]:
        for cat in entry['values']:
            if cat not in categorie_mappings:
                categorie_mappings[cat.lower()] = {entry['key']}
            else:
                categorie_mappings[cat.lower()].add(entry['key'])

    return categorie_mappings


def remap_categories(keywords):
    """
    Takes a list of keywords, maps these to their corresponding advaneo-categories and returns these as a list
    :param keywords: a list of keywords
    :return: a list of categories corresponding to the keywords
    """

    # checks if keywords are given
    if all([keywords is not None, keywords != "N/A"]):
        categorie_mapping = get_categorie_mapping()
        categories = []
        mapping_keys = categorie_mapping.keys()

        for keyword in keywords:
            keyword_lower = keyword["name"].lower()

            for key in mapping_keys:
                if key in keyword_lower:

                    for category in categorie_mapping[key]:
                        if category not in categories:
                            categories.append(category)
    else:
        # return only "OTHERS" if no keywords are given
        categories = ["OTHERS"]

    if not categories:
        categories = ["OTHERS"]

    return categories


with open("transformer/resources/termmapping.json", "rb") as f:
    mapping_categories = load(f)

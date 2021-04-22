def transform_group(group, portal):
    """
    Transformiert die Informationen der Gruppen der jeweiligen Portale
    und führt sie in das benötigte Format für die DB um.
    :param group: Die zu transformierenden Gruppen-Daten (Dictionary)
    :param portal: Der Portalsoftwaretyp (String)
    :return: Die Gruppen-Daten im standardisierten Format (Dictionary)
    """
    gruppe = None

    # Todo: Gruppe für Kategorien nutzen
    # check if group information is present
    if group:
        if portal == "cdkan":
            fields = ["display_name", "description", "image_display_url", "title", "name"]

            for field in fields:
                if field not in group:
                    print(field, group)
                    group[field] = None
                elif group[field] == "":
                    group[field] = None
                elif group[field] == " ":
                    group[field] = None

            titel = group["title"]
            name = group["name"]
            beschreibung = group["description"]

            # Todo: Problem, wenn None gesetzt wird. Schauen, wie das zu lösen ist.
            extra = None
        else:
            return None

        gruppe = {
            "gruppeName": name,
            "gruppeBeschreibung": beschreibung,
            "gruppeTitel": titel,
            "gruppeExtra": extra
        }

    return gruppe

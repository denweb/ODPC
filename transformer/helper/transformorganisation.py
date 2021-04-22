def transform_organisation(portal, org):
    """
    Transformiert die Organisationsdaten in ein standardisiertes Format.
    :param portal: Der Portalsoftwaretyp (String)
    :param org: Die Organisationsdaten (Dictionary | String)
    :return: Die Organisationsdaten im standardisierten Format
    """
    titel = None
    name = None
    beschreibung = None
    status = None
    kontakt = None
    extra = None

    # check if org information was given.
    if org:

        if portal == "cdkan":

            fields = ["description", "created", "title", "name", "is_organization", "state", "image_url",
                      "revision_id", "type", "id", "approval_status"]

            for field in fields:
                if field not in org:
                    org[field] = None
                elif org[field] == "":
                    org[field] = None
                elif org[field] == " ":
                    org[field] = None

            titel = org["title"]
            name = org["name"]
            beschreibung = org["description"]
            status = org["state"]
            kontakt = {
                "kontaktName": None,
                "kontaktEmail": None
            }
            extra = ", ".join([org["created"],
                               str(org["is_organization"]),
                               str(org["image_url"]),
                               str(org["revision_id"]),
                               str(org["type"]),
                               str(org["approval_status"])])

        elif portal == "arcgis":
            titel = org["name"]

    organisation = {
        "organisationName": name,
        "organisationBeschreibung": beschreibung,
        "organisationTitel": titel,
        "organisationStatus": status,
        "organisationKontakt": kontakt,
        "organisationExtra": extra
    }

    return organisation

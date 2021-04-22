from database.dbcon import DBConnection


def upload(data, instance_type):
    """
    Lädt transformierte Metadatensätze oder Portalinformationen in die Daten-DB
    :param data: Ein transformierter Metadaten (Dictionary)
    :param instance_type: Angabe, ob ein Metadatensatz oder Portalinformationen, geladen werden sollen (String)
    :return: Die ID des erstellten Datenbankeintrags
    """

    db = DBConnection("testdb.db")

    if instance_type == "meta":
        meta_id = db.create_metadatensatz(data)
        for endpunkt in data["endpunkte"]:
            endpunkt["metaDatensatz"] = meta_id
            db.create_rohdaten(endpunkt)

        result = meta_id
    else:
        result = db.create_portal(data)

    # Todo: Add to create-functions
    db.connection.commit()
    db.connection.close()

    return result

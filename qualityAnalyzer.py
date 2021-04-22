from database.dbcon import DBConnection
from ast import literal_eval
from framework.framework import get_portal_scores
from framework.metrikencsv import gen_csv_metrik
from framework.utility.db_helfer import get_dateiformat_ids
import re
import csv


def get_portal_ids(db):
    """
    Extrahiert alle Portal-IDs aus der Daten-DB
    :param db: Verbindungs zur Daten-DB (DBConnection Instanz)
    :return: Liste aller Portal-IDs
    """
    return [portal[0] for portal in db.get_portals_software()]


def get_valide_kontakte(db):
    """
    Extrahiert alle Kontaktdaten aus der Daten-DB und sortiert deren IDs nach Validität.
    :param db: Verbindungs zur Daten-DB (DBConnection Instanz)
    :return: Ein Dictionary mit Sets der vollständig, teilweise und nicht validen IDs
    """
    kontakte = db.get_tables_dict("kontakt")

    kont = {
        "beide": set(),
        "name": set(),
        "email": set()
    }

    regex = re.compile(r"[^@]+(@|(at))[^@]+\.[^@]+")

    for kontakt in kontakte:
        mail = regex.fullmatch(kontakt["kontaktEmail"])
        name = kontakt["kontaktName"] != "" and kontakt["kontaktName"] != "None"

        if name and mail:
            kont["beide"].add(kontakt["kontaktID"])
        elif name:
            kont["name"].add(kontakt["kontaktID"])
        elif mail:
            kont["email"].add(kontakt["kontaktID"])

    return kont


def get_akt_daten(db):
    """
    Extrahiert alle Datum-IDs aus der Daten-DB von Daten der Jahre '20 und '21
    :param db: Verbindungs zur Daten-DB (DBConnection Instanz)
    :return: Ein Set mit den aktiven Datum-IDs
    """
    akt_daten = set(datum["datumID"]
                    for datum in db.get_attr_where("datum", "datumID", "(datum LIKE '%2021%' OR datum LIKE '%2020%')"))

    return akt_daten


def get_source_error_fehler(db):
    """
    Extrahier alle Fehler-IDs aus der Daten-DB von Fehlern mit dem Code 'source-error'.
    :param db: Verbindungs zur Daten-DB (DBConnection Instanz)
    :return: Ein Set mit den 'source-error'-Fehler-IDs
    """
    se_fehler = {fehler["fehlerID"]
                 for fehler in db.get_attr_single("fehler", "fehlerID", "fehlerCode", "source-error")}

    return se_fehler


def get_vollst_fehler(db):
    """
    Extrahier alle Fehler-IDs aus der Daten-DB von Fehlern mit den Codes 'missing-value', 'missing-cless',
    'blank-row' sowie 'blank-label' und ordnet diese entsprechenden Kategorien zu.
    :param db: Verbindungs zur Daten-DB (DBConnection Instanz)
    :return: Ein Dictionary mit den Kategorien und deren zugeordneten Fehler-IDs in einem Set.
    """
    vollst_fehler = {
        "zelle": {fehler["fehlerID"]
                  for fehler in
                  db.get_attr_where("fehler", "fehlerID", "fehlerCode = 'missing-value' OR fehlerCode = 'missing-cell'")},
        "reihe": {fehler["fehlerID"]
                  for fehler in db.get_attr_single("fehler", "fehlerID", "fehlerCode", "blank-row")},
        "label": {fehler["fehlerID"]
                   for fehler in db.get_attr_single("fehler", "fehlerID", "fehlerCode", "blank-label")}
    }

    return vollst_fehler


def analyze():
    """
    Führt die Datenqualitätsuntersuchung nach dem in der Arbeit erstellten Framwork auf den gesamten Datenbestand der
    Daten-DB durch und speichert deren Ergebnisse in der framework-DB.
    """
    db = DBConnection("testdb.db")
    portals = get_portal_ids(db)

    kontakte = get_valide_kontakte(db)
    akt_daten = get_akt_daten(db)
    dateiformate_ids = get_dateiformat_ids(db)
    se_fehler = get_source_error_fehler(db)
    vollst_fehler = get_vollst_fehler(db)

    framework_db = DBConnection("framework.db")
    for portal in portals:
        get_portal_scores(db, framework_db,
                          portal, kontakte, akt_daten, dateiformate_ids, se_fehler, vollst_fehler)

    # res = [gen_csv_metrik(db, portal, kontakte, akt_daten, dateiformate_ids, se_fehler, vollst_fehler) for portal in
    #        portals if portal != 22]
    # res = [elem for elem in res if elem]
    db.connection.close()

    framework_db.connection.commit()
    framework_db.connection.close()

    # with open("results.csv", "w") as f:
    #     w = csv.DictWriter(f, list(res[0].keys()))
    #     w.writeheader()
    #     w.writerows(res)


if __name__ == '__main__':
    analyze()

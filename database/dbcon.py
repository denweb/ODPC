import os
import sqlite3


class DBConnection (object):
    def __init__(self, dbname):
        self.dbname = dbname
        self.connection = sqlite3.connect("C:/Users/Dennis/PycharmProjects/ODPC/database/{0}".format(dbname))
        self.cursor = self.connection.cursor()

    def create_portal(self, portal_data):
        portalTypID = self.get_id("portalTyp", portal_data["portalTyp"])
        betreiberTypID = self.get_id("betreiberTyp", portal_data["betreiberTyp"])
        elternInstanzID = self.get_id("elternInstanz", portal_data["elternInstanz"])

        sql = "INSERT INTO portal " \
              "(titel, url, notizen, portalTyp, betreiber, betreiberTyp, elternInstanz) " \
              "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')".format(
                                                                    portal_data["titel"],
                                                                    portal_data["url"],
                                                                    portal_data["notizen"],
                                                                    portalTypID,
                                                                    portal_data["betreiber"],
                                                                    betreiberTypID,
                                                                    elternInstanzID
                                                                )
        try:
            self.cursor.execute(sql)

            portal_id = self.cursor.lastrowid
        except:
            portal_id = 999999999

        return portal_id

    def create_metadatensatz(self, meta_data):
        kategorien_ids = [self.get_id("kategorie", kategorie) for kategorie in meta_data["kategorien"]]
        tags_ids = [self.get_id("tag", tag) for tag in meta_data["tags"]]
        erstelldatum_id = self.get_id("datum", meta_data["erstellDatum"])
        updatedatum_id = self.get_id("datum", meta_data["updateDatum"])
        lizenz_id = self.get_id("lizenz", meta_data["lizenz"])
        autor_id = self.get_id("kontakt", meta_data["autor"])
        verwalter_id = self.get_id("kontakt", meta_data["verwalter"])
        organisation_id = self.get_id("organisation", meta_data["organisation"])
        gruppen_ids = [self.get_id("gruppe", gruppe) for gruppe in meta_data["gruppen"]]

        sql = "INSERT INTO metaDatensatz " \
              "(titel, beschreibung, autor, verwalter, url, geo, " \
              "organisation, erstellDatum, updateDatum, gruppe, extra, lizenz, tags, kategorien, portal) " \
              "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', " \
              "'{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}')".format(meta_data["titel"],
                                                                                    meta_data["beschreibung"],
                                                                                    autor_id,
                                                                                    verwalter_id,
                                                                                    meta_data["url"],
                                                                                    meta_data["geo"],
                                                                                    organisation_id,
                                                                                    erstelldatum_id,
                                                                                    updatedatum_id,
                                                                                    gruppen_ids,
                                                                                    meta_data["extra"],
                                                                                    lizenz_id,
                                                                                    tags_ids,
                                                                                    kategorien_ids,
                                                                                    meta_data["portalID"])
        try:
            self.cursor.execute(sql)

            meta_data_id = self.cursor.lastrowid
        except:
            meta_data_id = 999999999

        return meta_data_id

    def create_rohdaten(self, roh_data):
        erstelldatum_id = self.get_id("datum", roh_data["erstellDatum"])
        updatedatum_id = self.get_id("datum", roh_data["updateDatum"])
        dateityp_id = self.get_id("dateiTyp", roh_data["dateiTyp"])

        sql = "INSERT INTO rohDatensatz " \
              "(link, online, dateiName, valide, beschreibung, dateiTyp, " \
              "dateiGröße, titel, erstellDatum, updateDatum, metaDatensatz, extras) " \
              "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', " \
              "'{7}', '{8}', '{9}', '{10}', '{11}')".format(roh_data["link"],
                                                            roh_data["online"],
                                                            roh_data["dateiName"],
                                                            2,
                                                            roh_data["beschreibung"],
                                                            dateityp_id,
                                                            roh_data["dateiGröße"],
                                                            roh_data["titel"],
                                                            erstelldatum_id,
                                                            updatedatum_id,
                                                            roh_data["metaDatensatz"],
                                                            roh_data["extras"])
        try:
            self.cursor.execute(sql)

            roh_data_id = self.cursor.lastrowid
        except:
            roh_data_id = 999999999

        return roh_data_id

    # Todo: Eventuell auch aufwändigere Felder vereinheitlichen?
    def get_id(self, table, values):

        try:
            # Todo: Testen, ob die jeweiligen Felder der richtige Abgeleich sind. Ggf verfeinern / anpassen.
            # case: table is lizenz
            if table == "lizenz":
                exists = self.check_exist(table, "lizenzTitel", values["lizenzTitel"])

                if exists:
                    attr_id = exists[0]
                else:
                    attr_id = self.create_attr_lizenz(values)

            # case: table is kontakt
            elif table == "kontakt":
                exists = self.check_exist(table, "kontaktEmail", values["kontaktEmail"])

                if exists:
                    attr_id = exists[0]
                else:
                    attr_id = self.create_attr_kontakt(values)

            # case: table is gruppe
            elif table == "gruppe":
                exists = self.check_exist(table, "gruppeName", values["gruppeName"])

                if exists:
                    attr_id = exists[0]
                else:
                    attr_id = self.create_attr_gruppe(values)

            # case: table is organisation
            elif table == "organisation":
                exists = self.check_exist(table, "organisationName", values["organisationName"])

                if exists:
                    attr_id = exists[0]
                else:
                    attr_id = self.create_attr_organisation(values)

            # case: table is a simple table with only 1 extra field
            else:
                exists = self.check_exist(table, table, values)

                if exists:
                    attr_id = exists[0]
                else:
                    attr_id = self.create_attr(table, values)
        # Todo: Add a second try if unque contraint is the problem. Easiest solution: Add second function.
        except:
            attr_id = 999999999

        return attr_id

    def check_exist(self, table, att_name, value):
        sql = "SELECT {0}ID " \
              "FROM {0} " \
              "WHERE {1}='{2}'".format(table, att_name, value)

        result = self.cursor.execute(sql).fetchone()

        return result

    def create_attr(self, table, value):

        sql = "INSERT INTO {0} " \
              "({0}) " \
              "VALUES('{1}')".format(table, value)

        self.cursor.execute(sql)
        attr_id = self.cursor.lastrowid

        return attr_id

    def create_attr_lizenz(self, values):

        sql = "INSERT INTO lizenz " \
              "(lizenzTitel, lizenzUrl) " \
              "VALUES('{0}', '{1}')".format(values["lizenzTitel"], values["lizenzUrl"])

        self.cursor.execute(sql)
        attr_id = self.cursor.lastrowid

        return attr_id

    def create_attr_kontakt(self, values):

        sql = "INSERT INTO kontakt " \
              "(kontaktName, kontaktEmail) " \
              "VALUES('{0}', '{1}')".format(values["kontaktName"], values["kontaktEmail"])

        self.cursor.execute(sql)
        attr_id = self.cursor.lastrowid

        return attr_id

    def create_attr_gruppe(self, values):

        sql = "INSERT INTO gruppe " \
              "(gruppeName, gruppeTitel, gruppeBeschreibung, gruppeExtra) " \
              "VALUES('{0}', '{1}', '{2}', '{3}')".format(values["gruppeName"],
                                                    values["gruppeTitel"],
                                                    values["gruppeBeschreibung"],
                                                    values["gruppeExtra"])

        self.cursor.execute(sql)
        attr_id = self.cursor.lastrowid

        return attr_id

    def create_attr_organisation(self, values):

        kontakt_id = self.get_id("kontakt", values["organisationKontakt"])

        sql = "INSERT INTO organisation " \
              "(organisationName, organisationBeschreibung, organisationTitel, " \
              "organisationStatus, organisationKontakt, organisationExtra) " \
              "VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(values["organisationName"],
                                                    values["organisationBeschreibung"],
                                                    values["organisationTitel"],
                                                    values["organisationStatus"],
                                                    kontakt_id,
                                                    values["organisationExtra"])

        self.cursor.execute(sql)
        attr_id = self.cursor.lastrowid

        return attr_id

    def create_attr_fehler(self, data_id, values):

        sql = "INSERT INTO fehler " \
              "(rohDatensatzID, fehlerCode, fehlerNachricht, fehlerTags, fehlerExtras) " \
              "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')".format(data_id,
                                                                 values["fehlerCode"],
                                                                 values["fehlerNachricht"],
                                                                 str(values["fehlerTags"]).replace("'",'"'),
                                                                 str(values["fehlerExtras"]))

        self.cursor.execute(sql)
        attr_id = self.cursor.lastrowid

        return attr_id

    def get_rawdata_links(self):

        sql = "SELECT rohDatensatzID, link " \
              "FROM rohDatensatz;"

        self.cursor.execute(sql)

        res = self.cursor.fetchall()

        return res

    def get_portals_software(self):
        sql = "SELECT portalID " \
              "FROM portal " \
              "WHERE portalTyp='2' or portalTyp='3' or portalTyp='4';"

        self.cursor.execute(sql)

        res = self.cursor.fetchall()

        return res

    def get_tables_dict_by_condition(self, tablename, col, value):
        sql = "SELECT * " \
              "FROM {0} " \
              "WHERE {1} = '{2}';".format(tablename, col, value)

        cursor = self.cursor
        cursor.row_factory = sqlite3.Row

        self.cursor.execute(sql)

        res = self.cursor.fetchall()

        return res

    def update_rawdata(self, id, data):
        res = True

        fehler = [self.create_attr_fehler(id, fehler) for fehler in data["fehler"]]
        dateityp_real_id = self.get_id("dateiTyp", data["dateiTypReal"])

        try:
            sql = "UPDATE rohDatensatz " \
                  "SET " \
                  "valide = '{1}', " \
                  "anzahlFehler = '{2}', " \
                  "fehler = '{3}', " \
                  "dateiGrößeReal = '{4}', " \
                  "online = '{5}', " \
                  "dateiTypReal = '{6}' " \
                  "WHERE rohDatensatzID = '{0}'".format(id,
                                                        data["valide"],
                                                        data["anzahlFehler"],
                                                        fehler,
                                                        data["dateiGrößeReal"],
                                                        data["online"],
                                                        dateityp_real_id)

            self.cursor.execute(sql)
        except Exception as e:
            print("upload fails:", e)
            res = False

        return res




dummy_portal = {
    "titel": "TestPortal1",
    "url": "www.testportal1.de",
    "notizen": "bla",
    "portalTyp": "CKAN",
    "betreiber": "Testbetreiber",
    "betreiberTyp": "Amt1",
    "elternInstanz": "WasWarDasNochMal?"
}

dummy_portal2 = {
    "titel": "TestPortal2",
    "url": "www.testportal2.de",
    "notizen": "bla2",
    "portalTyp": "CKAN",
    "betreiber": "Testbetreiber",
    "betreiberTyp": "Amt2",
    "elternInstanz": "WasWarDasNochMal?"
}

dummy_metadata = {
    "titel": "TestmetaData2",
    "beschreibung": "Testbeschreibung1",
    "autor": {
        "kontaktName": "Testautor2",
        "kontaktEmail": "TestEmail3"
    },
    "verwalter": {
        "kontaktName": "Testverwalter4",
        "kontaktEmail": "TestEmail5"
    },
    "url": "http://www.test123.de",
    "geo": None,
    "organisation": {
        "organisationName": "TestOrg1",
        "organisationBeschreibung": "Test Beschreibung Org 1",
        "organisationTitel": "TestTitelOrg1",
        "organisationStatus": "active",
        "organisationKontakt": {
            "kontaktName": "OrgKontakt1",
            "kontaktEmail": "OrgEmail1"
        },
        "organisationExtra": ""
    },
    "erstellDatum": "01.01.2020",
    "updateDatum": "01.01.2020",
    "gruppen":[{
        "gruppeName": "TestGruppe1",
        "gruppeTitel": "GrTitel1",
        "gruppeBeschreibung": "Beschreibung einer Gruppe1",
        "gruppeExtra": ""
    }],
    "extra": "extra Infos!",
    "lizenz":{
        "lizenzTitel": "TestLizenz1",
        "lizenzUrl": "www.testlizenz.de"
    },
    "tags": ["tag1", "tag2", "test1tag"],
    "kategorien": ["kat1", "testkat2", "Hallo"],
    "portalID": 2
}

dummy_rohdaten = {
    "link": "www.test.de/c.csv",
    "online": 1,
    "dateiName": "test.csv",
    "valide": "1",
    "beschreibung": "Testdatensatzbeschreibung",
    "dateiTyp": "CSV",
    "dateiGröße": 2,
    "titel": "titel der Datei",
    "erstellDatum": "01.01.2020",
    "updateDatum": "01.02.2020",
    "metaDatensatz": 1,
    "extras": "Ne"
}

"""
# Todo: Später, wenn Zeit.

def create_db(dbname):

    # build database
    connection = sqlite3.connect(dbname)

    # initiate cursor
    cursor = connection.cursor()

    # portal table
    portal_table = "CREATE TABLE portal(" \
                   "portalID INTEGER PRIMARY KEY," \
                   "titel TEXT NOT NULL," \
                   "url TEXT NOT NULL," \
                   "notizen TEXT," \
                   "betreiber TEXT," \
                   "betreiberTyp INTEGER," \
                   "elternInstanz INTEGER," \
                   "portalTyp INTEGER" \
                   ")"

    # elternInstanz table
    elternInstanz_table = "CREATE TABLE elternInstanz(" \
                          "elternInstanzID INTEGER PRIMARY KEY," \
                          "elternInstanz TEXT" \
                          ")"


    # portalTyp table
    portalTyp_table = "CREATE TABLE portalTyp(" \
                      "portalTypID INTEGER PRIMARY KEY," \
                      "portalTyp TEXT" \
                      ")"

    # betreiberTyp table
    betreiberTyp_table = "CREATE TABLE betreiberTyp(" \
                         "betreiberTypID INTEGER PRIMARY KEY," \
                         "betreiberTyp TEXT" \
                         ")"

    cursor.execute("".join([portal_table,
                            elternInstanz_table,
                            portalTyp_table,
                            betreiberTyp_table
                            ]))
    connection.commit()

    print("Database {0} created successfully.".format(dbname))


if not os.path.exists(dbname):
    create_db(dbname)
"""

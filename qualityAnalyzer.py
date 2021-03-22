from database.dbcon import DBConnection
from ast import literal_eval


def get_portal_ids(db):
    return [portal[0] for portal in db.get_portals_software()]


def get_metadataitems(db, portal):
    res = [dict(row) for row in db.get_tables_dict_by_condition("metaDatensatz", "portal", portal)]

    for meta in res:
        meta["gruppe"] = [dict(db.get_tables_dict_by_condition("gruppe", "gruppeID", gruppeid)[0])
                        for gruppeid in
                        [gruppeid for gruppeid in literal_eval(meta["gruppe"]) if gruppeid != 999999999]]
        meta["organisation"] = dict(db.get_tables_dict_by_condition("organisation", "organisationID", meta["organisation"])[0])
        meta["kategorien"] = literal_eval(meta["kategorien"])
        meta["autor"] = dict(db.get_tables_dict_by_condition("kontakt", "kontaktID", meta["autor"])[0])
        meta["verwalter"] = dict(db.get_tables_dict_by_condition("kontakt", "kontaktID", meta["verwalter"])[0])
        meta["erstellDatum"] = dict(db.get_tables_dict_by_condition("datum", "datumID", meta["erstellDatum"])[0])["datum"]
        meta["updateDatum"] = dict(db.get_tables_dict_by_condition("datum", "datumID", meta["updateDatum"])[0])["datum"]
        meta["lizenz"] = dict(db.get_tables_dict_by_condition("lizenz", "lizenzID", meta["lizenz"])[0])
        meta["tags"] = [dict(db.get_tables_dict_by_condition("tag", "tagID", tagid)[0])["tag"]
                        for tagid in
                        [tagid for tagid in literal_eval(meta["tags"]) if tagid != 999999999]]

    return res


def get_rohdaten(db, meta):
    res = [dict(row) for row in db.get_tables_dict_by_condition("rohDatensatz", "metaDatensatz", meta)]

    for roh in res:
        roh["erstellDatum"] = dict(db.get_tables_dict_by_condition("datum", "datumID", roh["erstellDatum"])[0])[
            "datum"]
        roh["updateDatum"] = dict(db.get_tables_dict_by_condition("datum", "datumID", roh["updateDatum"])[0])["datum"]
        roh["dateiTyp"] = dict(db.get_tables_dict_by_condition("dateiTyp", "dateiTypID", roh["dateiTyp"])[0])["dateiTyp"]
        if roh["fehler"]:
            roh["fehler"] = [dict(db.get_tables_dict_by_condition("fehler", "fehlerID", fehlerid)) for fehlerid
                             in roh["fehler"]]

    return res


dbPortals = DBConnection("testdb.db")
portals = get_portal_ids(dbPortals)

for portal in portals:
    metadaten = get_metadataitems(dbPortals, portal)
    rohdaten = [get_rohdaten(dbPortals, meta["metaDatensatzID"]) for meta in metadaten]

    data = {
        "meta": metadaten,
        "roh": rohdaten
    }

    print(data)

#metadaten = get_metadataitems(dbPortals, portals[0])
#rohdaten = get_rohdaten(dbPortals, metadaten[0]["metaDatensatzID"])

#print(rohdaten)


dbPortals.connection.close()


"""
data = {}
for portal in portals:
    data[portal] = {}
    data[portal]["meta"]= get_metadataitems(dbPortals, portal)
    for metaitem in data[portal]["meta"]:
        data[portal]["rohdaten"] = get_rohdaten(dbPortals, metaitem["metaDatensatzID"])

print(data)
"""
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


def get_metadataids(db, portal):
    return tuple(meta[0] for meta in db.get_meta_ids(portal))


def get_rohdataids_meta(db, meta):
    return tuple(roh[0] for roh in db.get_roh_ids_single(meta))


def get_rohdataids_list(db, meta):
    return tuple(roh[0] for roh in db.get_roh_ids_list(meta))


def get_attr_single(db, table, attr, condition, value):
    return db.get_attr_single(table, attr, condition, value)


def get_attr_list(db, table, attr, condition, values):
    return tuple(attr[0] for attr in db.get_attr_list(table, attr, condition, values))


def get_voll(db, portal_ids):
    pass


if __name__ == '__main__':
    dbPortals = DBConnection("testdb.db")
    portals = get_portal_ids(dbPortals)

    for portal in portals:
        meta_ids = get_metadataids(dbPortals, portal)
        roh_ids = get_rohdataids_list(dbPortals, meta_ids)

        portal_data = {
            "portal": portal,
            "meta": meta_ids,
            "roh": roh_ids
        }

    dbPortals.connection.close()

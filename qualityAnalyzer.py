from database.dbcon import DBConnection
from ast import literal_eval
from framework.framework import get_portal_scores


def get_portal_ids(db):
    return [portal[0] for portal in db.get_portals_software()]


def get_metadataitems(db, portal):
    res = [dict(row) for row in db.get_tables_dict_by_condition_single("metaDatensatz", "portal", portal)]

    for meta in res:
        meta["gruppe"] = [dict(db.get_tables_dict_by_condition_single("gruppe", "gruppeID", gruppeid)[0])
                        for gruppeid in
                        [gruppeid for gruppeid in literal_eval(meta["gruppe"]) if gruppeid != 999999999]]
        meta["organisation"] = dict(db.get_tables_dict_by_condition_single("organisation", "organisationID", meta["organisation"])[0])
        meta["kategorien"] = literal_eval(meta["kategorien"])
        meta["autor"] = dict(db.get_tables_dict_by_condition_single("kontakt", "kontaktID", meta["autor"])[0])
        meta["verwalter"] = dict(db.get_tables_dict_by_condition_single("kontakt", "kontaktID", meta["verwalter"])[0])
        meta["erstellDatum"] = dict(db.get_tables_dict_by_condition_single("datum", "datumID", meta["erstellDatum"])[0])["datum"]
        meta["updateDatum"] = dict(db.get_tables_dict_by_condition_single("datum", "datumID", meta["updateDatum"])[0])["datum"]
        meta["lizenz"] = dict(db.get_tables_dict_by_condition_single("lizenz", "lizenzID", meta["lizenz"])[0])
        meta["tags"] = [dict(db.get_tables_dict_by_condition_single("tag", "tagID", tagid)[0])["tag"]
                        for tagid in
                        [tagid for tagid in literal_eval(meta["tags"]) if tagid != 999999999]]

    return res


def get_rohdaten(db, meta):
    res = [dict(row) for row in db.get_tables_dict_by_condition_single("rohDatensatz", "metaDatensatz", meta)]

    for roh in res:
        roh["erstellDatum"] = dict(db.get_tables_dict_by_condition_single("datum", "datumID", roh["erstellDatum"])[0])[
            "datum"]
        roh["updateDatum"] = dict(db.get_tables_dict_by_condition_single("datum", "datumID", roh["updateDatum"])[0])["datum"]
        roh["dateiTyp"] = dict(db.get_tables_dict_by_condition_single("dateiTyp", "dateiTypID", roh["dateiTyp"])[0])["dateiTyp"]
        if roh["fehler"]:
            roh["fehler"] = [dict(db.get_tables_dict_by_condition_single("fehler", "fehlerID", fehlerid)) for fehlerid
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
    db = DBConnection("testdb.db")
    portals = get_portal_ids(db)

    for portal in portals:
        res = get_portal_scores(db, portal)

    db.connection.close()

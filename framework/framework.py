from framework.vollständigkeit import get_vollst
from framework.genauigkeit import get_genau
from framework.aktualität import get_akt


def get_metadataids(db, portal):
    return tuple(meta[0] for meta in db.get_meta_ids(portal))


def get_rohdataids_meta(db, meta):
    return tuple(roh[0] for roh in db.get_roh_ids_single(meta))


def get_rohdataids_list(db, meta):
    return tuple(roh[0] for roh in db.get_roh_ids_list(meta))


def get_datum_ids(db, meta):
    nested_daten = [(datensatz["erstellDatum"], datensatz["updateDatum"]) for datensatz in meta]
    datum_ids = set(datum for element in nested_daten for datum in element if datum != 4)

    return datum_ids


def get_portal_scores(db, portal, kontakte, akt_daten):
    meta_ids = get_metadataids(db, portal)
    roh_ids = get_rohdataids_list(db, meta_ids)

    meta = tuple(db.get_tables_dict_by_condition_list("metaDatensatz", "metaDatensatzID", meta_ids))
    roh = tuple(db.get_tables_dict_by_condition_list("rohDatensatz", "rohDatensatzID", roh_ids))

    datum_ids = get_datum_ids(db, meta)

    if meta:
        genau = get_genau(meta, kontakte)
        vollst = get_vollst(meta)
        akt = get_akt(meta, akt_daten, datum_ids)



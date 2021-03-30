from framework.vollständigkeit import get_vollst
from framework.genauigkeit import get_genau
from framework.aktualität import get_akt
from framework.abrufbarkeit import get_abr
from framework.offenheit import get_off
from framework.kontaktierbarkeit import get_kon
from framework.rückverfolgbarkeit import get_rue
from framework.validität import get_val
from framework.diversität import get_div
from urllib.parse import urlparse
from framework.utility.db_helfer import gen_sql


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


def get_portal_scores(db, framework_db, portal, kontakte, akt_daten, dateiformate_ids, se_fehler, vollst_fehler):
    meta_ids = get_metadataids(db, portal)
    roh_ids = get_rohdataids_list(db, meta_ids)

    meta = tuple(db.get_tables_dict_by_condition_list("metaDatensatz", "metaDatensatzID", meta_ids))
    roh = tuple(db.get_tables_dict_by_condition_list("rohDatensatz", "rohDatensatzID", roh_ids))
    portal_domain = urlparse(db.get_attr_single("portal", "url", "portalID", portal)[0]["url"]).netloc

    datum_ids = get_datum_ids(db, meta)


    if meta:
        genau = get_genau(meta, kontakte)
        gen_sql(genau, "Genauigkeit")
        vollst = get_vollst(meta, roh, vollst_fehler)
        gen_sql(vollst, "Vollständigkeit")
        akt = get_akt(meta, akt_daten, datum_ids)
        abr = get_abr(roh, portal_domain)
        off = get_off(meta, roh, dateiformate_ids)
        kon = get_kon(meta, kontakte)
        rue = get_rue(meta)
        val = get_val(roh, se_fehler)
        div = get_div(meta, roh)

        #print(genau, div, vollst, akt, abr, off, kon, rue, val)
        #print()



from framework.vollständigkeit import get_vollst
from framework.genauigkeit import get_genau
from framework.aktualität import get_akt
from framework.abrufbarkeit import get_abr
from framework.offenheit import get_off
from framework.kontaktierbarkeit import get_kon
from framework.rückverfolgbarkeit import get_rue
from framework.validität import get_val
from framework.diversität import get_div
from framework.portalEbene import get_portal_metriken
from framework.metaEbene import get_meta_metriken
from framework.rohEbene import get_roh_metriken
from urllib.parse import urlparse
from framework.utility.db_helfer import gen_sql


def get_metadataids(db, portal):
    """
    Liefert die IDs aller Metadaten-Einträge eines Portals in der Daten-DB.
    """
    return tuple(meta[0] for meta in db.get_meta_ids(portal))


def get_rohdataids_list(db, meta):
    """
    Liefert die IDs aller Rohdaten-Einträge eines Metadaten-Eintrags in der Daten-DB.
    """
    return tuple(roh[0] for roh in db.get_roh_ids_list(meta))


def get_datum_ids(meta):
    """
    Liefert die IDs der Erstell- und Update-Daten jedes Metadatensatzes eines Datenportals. (Aus der Daten DB.)
    """
    nested_daten = [(datensatz["erstellDatum"], datensatz["updateDatum"]) for datensatz in meta]
    datum_ids = set(datum for element in nested_daten for datum in element if datum != 3)

    return datum_ids


def get_portal_scores(db, framework_db, portal, kontakte, akt_daten, dateiformate_ids, se_fehler, vollst_fehler):
    """
    Berechnet für ein OGD-Portal in der DB die Qualitätswerte, wie sie im Framework definiert sind
    und lädt diese Ergebnisse in die framework.db
    :param db: Die Verbindung zur Daten-Datenbank (DBConnection Instanz)
    :param framework_db: Die Verbindung zur Framework-Datenbank (DBConnection Instanz)
    :param portal: DB ID des zu untersuchenden Portals (INT)
    :param kontakte: IDs von validen Kontakten in der Daten-DB (Dict)
    :param akt_daten: IDs von Datums-Einträgen aus den Jahren '20 und '21 in der Daten-DB (Set)
    :param dateiformate_ids: IDs von maschinenlesbaren und nicht-proprietären Dateitypen in der Daten-DB (Dict)
    :param se_fehler: IDs von 'system-error'-Fehlern in der Daten-DB (Set)
    :param vollst_fehler: IDs von Fehlern, die die Vollständigkeit betreffen, in der Daten-DB (Dict)
    """
    meta_ids = get_metadataids(db, portal)
    roh_ids = get_rohdataids_list(db, meta_ids)

    meta = tuple(db.get_tables_dict_by_condition_list("metaDatensatz", "metaDatensatzID", meta_ids))
    roh = tuple(db.get_tables_dict_by_condition_list("rohDatensatz", "rohDatensatzID", roh_ids))
    portal_domain = urlparse(db.get_attr_single("portal", "url", "portalID", portal)[0]["url"]).netloc

    datum_ids = get_datum_ids(meta)

    if meta:
        genau = get_genau(meta, kontakte, portal)
        framework_db.create_framework(gen_sql(genau, "Genauigkeit"))

        vollst = get_vollst(meta, roh, vollst_fehler, portal)
        framework_db.create_framework(gen_sql(vollst, "Vollständigkeit"))

        akt = get_akt(meta, akt_daten, datum_ids, portal)
        framework_db.create_framework(gen_sql(akt, "Aktualität"))

        abr = get_abr(roh, portal_domain, portal)
        framework_db.create_framework(gen_sql(abr, "Abrufbarkeit"))

        off = get_off(meta, roh, dateiformate_ids, portal)
        framework_db.create_framework(gen_sql(off, "Offenheit"))

        kon = get_kon(meta, kontakte, portal)
        framework_db.create_framework(gen_sql(kon, "Kontaktierbarkeit"))

        rue = get_rue(meta, portal)
        framework_db.create_framework(gen_sql(rue, "Rückverfolgbarkeit"))

        val = get_val(roh, se_fehler, portal)
        framework_db.create_framework(gen_sql(val, "Validität"))

        div = get_div(meta, roh, portal)
        framework_db.create_framework(gen_sql(div, "Diversität"))

        portalEbene = get_portal_metriken(portal, akt, div, abr)
        framework_db.create_framework(gen_sql(portalEbene, "portalEbene"))

        metaEbene = get_meta_metriken(portal, genau, vollst, akt, abr, off, kon, rue)
        framework_db.create_framework(gen_sql(metaEbene, "metaEbene"))

        rohEbene = get_roh_metriken(portal, vollst, off, val)
        framework_db.create_framework(gen_sql(rohEbene, "rohEbene"))

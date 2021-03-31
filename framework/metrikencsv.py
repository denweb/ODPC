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
from framework.framework import get_metadataids, get_rohdataids_list, get_datum_ids
from urllib.parse import urlparse


def gen_csv_metrik(db, portal, kontakte, akt_daten, dateiformate_ids, se_fehler, vollst_fehler):
    res = None

    meta_ids = get_metadataids(db, portal)
    roh_ids = get_rohdataids_list(db, meta_ids)

    meta = tuple(db.get_tables_dict_by_condition_list("metaDatensatz", "metaDatensatzID", meta_ids))
    roh = tuple(db.get_tables_dict_by_condition_list("rohDatensatz", "rohDatensatzID", roh_ids))
    portal_domain = urlparse(db.get_attr_single("portal", "url", "portalID", portal)[0]["url"]).netloc

    datum_ids = get_datum_ids(db, meta)

    if meta:
        genau = get_genau(meta, kontakte, portal)
        vollst = get_vollst(meta, roh, vollst_fehler, portal)
        akt = get_akt(meta, akt_daten, datum_ids, portal)
        abr = get_abr(roh, portal_domain, portal)
        off = get_off(meta, roh, dateiformate_ids, portal)
        kon = get_kon(meta, kontakte, portal)
        rue = get_rue(meta, portal)
        val = get_val(roh, se_fehler, portal)
        div = get_div(meta, roh, portal)
        portalEbene = get_portal_metriken(portal, akt, div, abr)
        metaEbene = get_meta_metriken(portal, genau, vollst, akt, abr, off, kon, rue)
        rohEbene = get_roh_metriken(portal, vollst, off, val)

        res = {
            "Portal": portal,
            "Portalsoftware": 0,
            "DS": len(meta),
            "Roh_pro_DS": len(roh)/len(meta),
            "Titel_Länge": 0,
            "Beschreibung_DS": 0,
            "Beschreibung_DS_Anteil": 0,
            "Beschreibung_Länge": 0,
            "Kontakte_einz": 0,
            "Kontakte_valide_Anteil": 0,
            "DS_Kontakte_valide_Anteil": 0,
            "URL_einz": 0,
            "DS_URL": 0,
            "DS_URL_Anteil": 0,
            "DS_geo": 0,
            "DS_geo_Anteil": 0,
            "DS_Erstelldatum": 0,
            "DS_Erstelldatum_Anteil": 0,
            "Erstelldatum_Zeitspanne": 0,
            "DS_Updatedatum": 0,
            "DS_Updatedatum_Anteil": 0,
            "Updatedatum_Zeitspanne": 0,
            "Updatedatum_ung_Erstelldatum": 0,
            "Updatedatum_ung_Erstelldatum_Anteil": 0,
            "Tags": 0,
            "Tags_einz": 0,
            "DS_mit_Tags": 0,
            "DS_mit_Tags_Anteil": 0,
            "Tags_pro_DS_Durchschnitt": 0,
            "Gruppen": 0,
            "Gruppen_einzig": 0,
            "DS_mit_Gruppen": 0,
            "DS_mit_Gruppen_Anteil": 0,
            "Gruppen_pro_DS_Durchschnitt": 0,
            "Lizenzen_einz": 0,
            "Lizenzen_offen_Anteil": 0,
            "DS_mit_Lizenz": 0,
            "DS_mit_Lizenz_Anteil": 0,
            "DS_mit_Lizenz_offen": 0,
            "DS_mit_Lizenz_offen_Anteil": 0,
            "Roh": len(roh),
            "Link_intern_Anteil": 0,
            "online": 0,
            "online_Anteil": 0,
            "offline": 0,
            "offline_Anteil": 0,
            "Name_Anteil": 0,
            "Name_einz": 0,
            "Name_einz_Länge": 0,
            "DS_Name_einz_Anteil": 0,
            "valid_0": 0,
            "valid_0_Anteil": 0,
            "valid_1": 0,
            "valid_1_Anteil": 0,
            "valid_2": 0,
            "valid_2_Anteil": 0,
            "valid_3": 0,
            "valid_3_Anteil": 0,
            "valid_4": 0,
            "valid_4_Anteil": 0,
            "valid_5": 0,
            "valid_5_Anteil": 0,
            "Beschreibung_Roh": 0,
            "Beschreibung_Roh_Anteil": 0,
            "Beschreibung_Roh_Länge": 0,
            "Fehler_Durchschnitt": 0,
            "Fehler_pro_Roh_Durchschnitt": 0,
            "Dateityp_einzig": 0,
            "Dateityp_gegeben_Anteil": 0,
            "DateitypReal_gegeben_Anteil": 0,
            "DateitypReal_einzig_Roh_Durchschnitt": 0,
            "Roh_ML": 0,
            "Roh_ML_Anteil": 0,
            "Roh_offen": 0,
            "Roh_offen_Anteil": 0,
            "Roh_Erstelldatum": 0,
            "Roh_Erstelldatum_Anteil": 0,
            "Roh_Erstelldatum_Zeitspanne": 0,
            "Roh_Updatedatum": 0,
            "Roh_Updatedatum_Anteil": 0,
            "Roh_Updatedatum_Zeitspanne": 0,
            "Roh_Updatedatum_ung_Erstelldatum": 0,
            "Roh_Updatedatum_ung_Erstelldatum_Anteil": 0,
            "Roh_validierbar": 0,
            "Roh_validierbar_Anteil": 0,
            "Fehler_validierbar_Durchschnitt": 0,
            "Rohdaten_Fehler_Zelle": 0,
            "Rohdaten_Fehler_Zelle_Anteil": 0,
            "Rohdaten_Fehler_Reihe": 0,
            "Rohdaten_Fehler_Reihe_Anteil": 0,
            "Rohdaten_Fehler_Label": 0,
            "Rohdaten_Fehler_Label_Anteil": 0,
            "Fehler_Zelle": 0,
            "Fehler_Zelle_Anteil": 0,
            "Fehler_Reihe": 0,
            "Fehler_Reihe_Anteil": 0,
            "Fehler_Label": 0,
            "Fehler_Label_Anteil": 0,
            "Dateigröße_Durchschnitt": 0,
            "Dateigröße_min": 0,
            "Dateigröße_max": 0,
            "Dateigröße_Summe": 0,
        }
        for framew in [
            (genau, "gen_"),
            (vollst, "vollst_"),
            (akt, "akt_"),
            (abr, "abr_"),
            (off, "off_"),
            (kon, "kon_"),
            (rue, "rue_"),
            (val, "val_"),
            (div, "div_"),
            (portalEbene, "portalEbene_"),
            (metaEbene, "metaEbene_"),
            (rohEbene, "rohEbene_"),
        ]:
            for metr in framew[0]:
                if metr != "portalID":
                    res["".join([framew[1], metr])] = framew[0][metr]

    return res

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
from framework.utility.lizenzen import nicht_offen
from urllib.parse import urlparse
from statistics import mean
from ast import literal_eval
import traceback


# Todo: Fix Anteile > 1
def gen_csv_metrik(db, portal, kontakte, akt_daten, dateiformate_ids, se_fehler, vollst_fehler):
    """
    Für die Erstellung der Framework-Metriken in einer Übersichts-CSV. Internes Hilfsmittel für die Visualisierung.
    """
    res = None

    meta_ids = get_metadataids(db, portal)
    roh_ids = get_rohdataids_list(db, meta_ids)

    meta = tuple(db.get_tables_dict_by_condition_list("metaDatensatz", "metaDatensatzID", meta_ids))
    roh = tuple(db.get_tables_dict_by_condition_list("rohDatensatz", "rohDatensatzID", roh_ids))
    portal_domain = urlparse(db.get_attr_single("portal", "url", "portalID", portal)[0]["url"]).netloc
    portalsoftware = db.get_attr_single("portal", "portalTyp", "portalID", portal)[0]["portalTyp"]

    datum_ids = get_datum_ids(db, meta)

    # for data in roh:
    #     print(type(data["fehler"]))

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

        anz_fehler = 0
        try:
            anz_fehler = sum([int(data["anzahlFehler"]) for data in roh
                              if all([data["anzahlFehler"] != "None",
                                      data["anzahlFehler"] != 0,
                                      data["anzahlFehler"] is not None])])
        except Exception:
            pass

        res = {
            "Portal": portal,
            "Portalsoftware": portalsoftware,
            "DS": len(meta),
            "Roh_pro_DS": len(roh)/len(meta),
            "Titel_Laenge": mean([len(data["titel"]) for data in meta]),
            "Beschreibung_DS": len([1 for data in meta if data["beschreibung"] != "None"]),
            "Beschreibung_DS_Anteil": 0,
            "Beschreibung_Laenge": mean([len(data["beschreibung"]) for data in meta if data["beschreibung"] != "None"]),
            "Autor_einz": len({data["autor"] for data in meta}),
            "DS_Autor_valide": len([1 for data in meta
                                    if any([data["autor"] in kontakte["name"], data["autor"] in kontakte["email"]])]),
            "DS_Autor_valide_Anteil": 0,
            "Verwalter_einz": len({data["autor"] for data in meta}),
            "DS_Verwalter_valide": len([1 for data in meta
                                        if any([data["verwalter"] in kontakte["name"],
                                                data["verwalter"] in kontakte["email"]])]),
            "DS_Verwalter_valide_Anteil": 0,
            "URL_einz": len({data["url"] for data in meta if data["url"] != "None"}),
            "DS_URL": len([1 for data in meta if data["url"] != "None"]),
            "DS_URL_Anteil": 0,
            "DS_geo": len([1 for data in meta if data["geo"] != "None"]),
            "DS_geo_Anteil": 0,
            "DS_Erstelldatum":  len([1 for data in meta if data["erstellDatum"] != 3]),
            "DS_Erstelldatum_Anteil": 0,
            "Erstelldatum_Zeitspanne": 0,
            "DS_Updatedatum": len([1 for data in meta if data["updateDatum"] != 3]),
            "DS_Updatedatum_Anteil": 0,
            "Updatedatum_Zeitspanne": 0,
            "Updatedatum_ung_Erstelldatum": len([1 for data in meta
                                                 if all([data["updateDatum"] != 3, data["erstellDatum"] != 3,
                                                         data["updateDatum"] != data["erstellDatum"]])]),
            "Updatedatum_ung_Erstelldatum_Anteil": 0,
            "Tags": sum([len(literal_eval(data["tags"])) for data in meta]),
            "Tags_einz": len({tag for data in meta for tag in literal_eval(data["tags"])}),
            "DS_mit_Tags": len([1 for data in meta if literal_eval(data["tags"])]),
            "DS_mit_Tags_Anteil": 0,
            "Tags_pro_DS_Durchschnitt": 0,
            "Gruppen": sum([len(literal_eval(data["gruppe"])) for data in meta]),
            "Gruppen_einzig": len({tag for data in meta for tag in literal_eval(data["gruppe"])}),
            "DS_mit_Gruppen": len([1 for data in meta if literal_eval(data["gruppe"])]),
            "DS_mit_Gruppen_Anteil": 0,
            "Gruppen_pro_DS_Durchschnitt": 0,
            "Lizenzen_einz": len({data["lizenz"] for data in meta if data["lizenz"] != 2}),
            "Lizenzen_offen_Anteil": 0,
            "DS_mit_Lizenz": len([1 for data in meta if data["lizenz"] != 2]),
            "DS_mit_Lizenz_Anteil": 0,
            "DS_mit_Lizenz_offen": len([1 for data in meta if data["lizenz"] not in nicht_offen]),
            "DS_mit_Lizenz_offen_Anteil": 0,
            "Roh": len(roh),
            "Link_intern_Anteil": len([1 for data in roh if portal_domain in data["link"]]) / len(roh),
            "online": len([1 for data in roh if data["online"] == "True"]),
            "online_Anteil": 0,
            "offline": 0,
            "offline_Anteil": 0,
            "Name_Anteil": len([1 for data in roh if data["dateiName"] != "None"]) / len(roh),
            "Name_einz": len({data["dateiName"] for data in roh if data["dateiName"] != "None"}),
            "Name_einz_Laenge": 0,
            "DS_Name_einz_Anteil": 0,
            "valid_0": len([1 for data in roh if data["valide"] == 0]),
            "valid_0_Anteil": 0,
            "valid_1": len([1 for data in roh if data["valide"] == 1]),
            "valid_1_Anteil": 0,
            "valid_2": len([1 for data in roh if data["valide"] == 2]),
            "valid_2_Anteil": 0,
            "valid_3": len([1 for data in roh if data["valide"] == 3]),
            "valid_3_Anteil": 0,
            "valid_4": len([1 for data in roh if data["valide"] == 4]),
            "valid_4_Anteil": 0,
            "valid_5": len([1 for data in roh if data["valide"] == 5]),
            "valid_5_Anteil": 0,
            "Beschreibung_Roh": len([1 for data in roh if data["beschreibung"] != "None"]),
            "Beschreibung_Roh_Anteil": 0,
            "Beschreibung_Roh_Laenge": 0,
            "Fehler_Durchschnitt": 0,
            "Fehler_pro_Roh_Durchschnitt": 0,
            "Dateityp_einz": len({data["dateiTyp"] for data in roh if data["dateiTyp"] != 1}),
            "Dateityp_gegeben_Anteil": 0,
            "DateitypReal_einz": len({data["dateiTypReal"] for data in roh if data["dateiTypReal"] != 1}),
            "DateitypReal_gegeben_Anteil": 0,
            "DateitypReal_einz_DS_Durchschnitt": get_df_mean(roh),
            "Roh_ML": len([1 for data in roh if data["dateiTypReal"] in dateiformate_ids["dateiformate_mr"]]),
            "Roh_ML_Anteil": 0,
            "Roh_offen": len([1 for data in roh if data["dateiTypReal"] in dateiformate_ids["dateiformate_np"]]),
            "Roh_offen_Anteil": 0,
            "Roh_Erstelldatum": len([1 for data in roh if data["erstellDatum"] != 3]),
            "Roh_Erstelldatum_Anteil": 0,
            "Roh_Erstelldatum_Zeitspanne": 0,
            "Roh_Updatedatum": len([1 for data in roh if data["updateDatum"] != 3]),
            "Roh_Updatedatum_Anteil": 0,
            "Roh_Updatedatum_Zeitspanne": 0,
            "Roh_Updatedatum_ung_Erstelldatum": len([1 for data in roh
                                                     if all([data["updateDatum"] != 3, data["erstellDatum"] != 3,
                                                             data["updateDatum"] != data["erstellDatum"]])]),
            "Roh_Updatedatum_ung_Erstelldatum_Anteil": 0,
            "Roh_validierbar": len([1 for data in roh if data["anzahlFehler"] != "None"]),
            "Roh_validierbar_Anteil": 0,
            "Fehler_validierbar_Durchschnitt": 0,
            "Roh_Fehler_Zelle": get_fehler_metr(roh, vollst_fehler, "zelle"),
            "Roh_Fehler_Zelle_Anteil": 0,
            "Roh_Fehler_Reihe": get_fehler_metr(roh, vollst_fehler, "reihe"),
            "Roh_Fehler_Reihe_Anteil": 0,
            "Roh_Fehler_Label": get_fehler_metr(roh, vollst_fehler, "label"),
            "Roh_Fehler_Label_Anteil": 0,
            "Fehler_Zelle": get_fehler_counts(roh, vollst_fehler, "zelle"),
            "Fehler_Zelle_Anteil": 0,
            "Fehler_Reihe": get_fehler_counts(roh, vollst_fehler, "reihe"),
            "Fehler_Reihe_Anteil": 0,
            "Fehler_Label": get_fehler_counts(roh, vollst_fehler, "label"),
            "Fehler_Label_Anteil": 0,
            "Dateigroesse_Durchschnitt": 0,
            "Dateigroesse_min": 0,
            "Dateigroesse_max": 0,
            "Dateigroesse_Summe": 0,
        }

        # Anteile - Meta
        res["Beschreibung_DS_Anteil"] = res["Beschreibung_DS"] / res["DS"]
        res["DS_Autor_valide_Anteil"] = res["DS_Autor_valide"] / res["DS"]
        res["DS_Verwalter_valide_Anteil"] = res["DS_Verwalter_valide"] / res["DS"]
        res["DS_URL_Anteil"] = res["DS_URL"] / res["DS"]
        res["DS_geo_Anteil"] = res["DS_geo"] / res["DS"]
        res["DS_Erstelldatum_Anteil"] = res["DS_Erstelldatum"] / res["DS"]
        res["DS_Updatedatum_Anteil"] = res["DS_Updatedatum"] / res["DS"]
        res["Updatedatum_ung_Erstelldatum_Anteil"] = res["Updatedatum_ung_Erstelldatum"] / res["DS"]
        res["DS_mit_Tags_Anteil"] = res["DS_mit_Tags"] / res["DS"]
        res["Tags_pro_DS_Durchschnitt"] = res["Tags"] / res["DS"]
        res["DS_mit_Gruppen_Anteil"] = res["DS_mit_Gruppen"] / res["DS"]
        res["Gruppen_pro_DS_Durchschnitt"] = res["Gruppen"] / res["DS"]
        if res["Lizenzen_einz"] != 0:
            res["Lizenzen_offen_Anteil"] = len({data["lizenz"] for data in meta if data["lizenz"] not in nicht_offen}) \
                                           / res["Lizenzen_einz"]
        res["DS_mit_Lizenz_Anteil"] = res["DS_mit_Lizenz"] / res["DS"]
        res["DS_mit_Lizenz_offen_Anteil"] = res["DS_mit_Lizenz_offen"] / res["DS"]

        # Weiteres Roh
        res["online_Anteil"] = res["online"] / res["Roh"]
        res["offline"] = res["Roh"] - res["online"]
        res["offline_Anteil"] = res["offline"] / res["Roh"]
        try:
            res["Name_einz_Laenge"] = mean({len(data["dateiName"]) for data in roh if data["dateiName"] != "None"})
        except Exception:
            pass
        res["DS_Name_einz_Anteil"] = res["Name_einz"] / res["Roh"]
        res["valid_0_Anteil"] = res["valid_0"] / res["Roh"]
        res["valid_1_Anteil"] = res["valid_1"] / res["Roh"]
        res["valid_2_Anteil"] = res["valid_2"] / res["Roh"]
        res["valid_3_Anteil"] = res["valid_3"] / res["Roh"]
        res["valid_4_Anteil"] = res["valid_4"] / res["Roh"]
        res["valid_5_Anteil"] = res["valid_5"] / res["Roh"]
        res["Beschreibung_Roh_Anteil"] = res["Beschreibung_Roh"] / res["Roh"]
        try:
            res["Beschreibung_Roh_Laenge"] = \
                mean([len(data["beschreibung"]) for data in roh if data["beschreibung"] != "None"])
        except Exception:
            pass
        try:
            res["Fehler_Durchschnitt"] = mean([int(data["anzahlFehler"]) for data in roh
                                               if all([data["anzahlFehler"] != "None",
                                                       data["anzahlFehler"] != 0,
                                                       data["anzahlFehler"] is not None])])
        except Exception:
            pass
        try:
            res["Fehler_pro_Roh_Durchschnitt"] = mean([int(data["anzahlFehler"]) for data in roh
                                                       if all([data["anzahlFehler"] != "None",
                                                               data["anzahlFehler"] != 0,
                                                               data["anzahlFehler"] is not None])])
        except Exception:
            pass
        res["Dateityp_gegeben_Anteil"] = len([1 for data in roh if data["dateiTyp"] != 1]) / res["Roh"]
        res["DateitypReal_gegeben_Anteil"] = len([1 for data in roh if data["dateiTypReal"] != 1]) / res["Roh"]
        res["Roh_ML_Anteil"] = res["Roh_ML"] / res["Roh"]
        res["Roh_offen_Anteil"] = res["Roh_offen"] / res["Roh"]
        res["Roh_Erstelldatum_Anteil"] = res["Roh_Erstelldatum"] / res["Roh"]
        res["Roh_Updatedatum_Anteil"] = res["Roh_Updatedatum"] / res["Roh"]
        res["Roh_Updatedatum_ung_Erstelldatum_Anteil"] = res["Roh_Updatedatum_ung_Erstelldatum"] / res["Roh"]
        res["Roh_validierbar_Anteil"] = res["Roh_validierbar"] / res["Roh"]
        try:
            res["Fehler_validierbar_Durchschnitt"] = mean([int(data["anzahlFehler"]) for data in roh
                                                           if all([data["anzahlFehler"] != "None",
                                                                  data["anzahlFehler"] is not None])])
        except Exception:
            traceback.print_exc()
        if res["Roh_validierbar"] > 0:
            res["Roh_Fehler_Zelle_Anteil"] = res["Roh_Fehler_Zelle"] / res["Roh_validierbar"]
            res["Roh_Fehler_Reihe_Anteil"] = res["Roh_Fehler_Reihe"] / res["Roh_validierbar"]
            res["Roh_Fehler_Label_Anteil"] = res["Roh_Fehler_Label"] / res["Roh_validierbar"]
        if anz_fehler > 0:
            res["Fehler_Zelle_Anteil"] = res["Fehler_Zelle"] / anz_fehler
            res["Fehler_Reihe_Anteil"] = res["Fehler_Reihe"] / anz_fehler
            res["Fehler_Label_Anteil"] = res["Fehler_Label"] / anz_fehler
        groess = get_size_metr(roh)
        for metr in groess:
            res[metr] = groess[metr]

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

        res["gesamt_score"] = sum([res["gen_gewScore"], res["vollst_gewScore"], res["akt_gewScore"],
                                   res["abr_gewScore"], res["off_gewScore"], res["kon_gewScore"],
                                   res["rue_gewScore"], res["val_gewScore"], res["div_gewScore"]
                                   ])
        res["gesamt_score_ebenen"] = sum([res["rohEbene_score"], res["metaEbene_score"], res["portalEbene_score"]])

    return res


def get_df_mean(roh):
    df_counter = {}
    for data in roh:
        if all([data["dateiTypReal"], data["dateiTypReal"] != 1]):
            if data["metaDatensatz"] not in df_counter:
                df_counter[data["metaDatensatz"]] = {data["dateiTypReal"]}
            else:
                df_counter[data["metaDatensatz"]].add(data["dateiTypReal"])

    df = [len(df_counter[d]) for d in df_counter]
    res = mean(df)

    return res


def get_fehler_metr(roh, vollst_fehler, typ):
    c = 0
    for data in roh:
        if all([data["fehler"] != "None", data["fehler"] is not None]):
            fehler = set(literal_eval(data["fehler"]))

            if fehler.intersection(vollst_fehler[typ]):
                c += 1

    return c


def get_fehler_counts(roh, vollst_fehler, typ):
    c = 0
    for data in roh:
        if all([data["fehler"] != "None", data["fehler"] is not None]):
            fehlers = literal_eval(data["fehler"])

            for fehler in fehlers:
                if fehler in vollst_fehler[typ]:
                    c += 1

    return c


def get_size_metr(roh):
    res = {
        "Dateigroesse_Durchschnitt": 0,
        "Dateigroesse_min":0,
        "Dateigroesse_max": 0,
        "Dateigroesse_Summe": 0
    }

    groess = [data["dateiGrößeReal"] for data in roh
              if all([data["dateiGrößeReal"] != "None",
                      data["dateiGrößeReal"] != 0,
                      data["dateiGrößeReal"] is not None])]

    if groess:
        res["Dateigroesse_Durchschnitt"] = mean(groess)
        res["Dateigroesse_min"] = min(groess)
        res["Dateigroesse_max"] = max(groess)
        res["Dateigroesse_Summe"] = sum(groess)

    return res

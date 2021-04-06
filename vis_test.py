import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

sns.set_style("whitegrid")


def get_titel_laenge_ds():
    plt.clf()

    plt.subplot(131)
    df.boxplot("Titel_Laenge", grid=False)
    plt.ylim(ymin=0)
    plt.subplot(132)
    df.boxplot("Beschreibung_DS_Anteil", grid=False)
    plt.ylim(ymin=0)
    plt.subplot(133)
    df.boxplot("Beschreibung_Laenge", grid=False)
    plt.ylim(ymin=0)

    plt.show()

    plt.savefig("plots/{}.png".format("DS_Titel_Laenge"))


def get_graphs(cols, rot=0, name="", ylim=False, draw=False, sub=False):
    c = 0
    if not sub:
        for col in cols:
            c += 1
            if isinstance(col, list):
                plt.clf()

                df.boxplot(
                    column=[subcol for subcol in col],
                    grid=False, rot=rot)

                if ylim:
                    plt.ylim(ymin=0)

                if draw:
                    plt.show()
                if name:
                    fname = "_".join([name, str(c)])
                else:
                    fname = str(col)[1:-2].replace("'", "")
                plt.savefig("plots/{}.png".format(fname))

            else:
                plt.clf()

                df.boxplot(
                    column=[col],
                    grid=False)

                if ylim:
                    plt.ylim(ymin=0)

                if draw:
                    plt.show()

                if name:
                    fname = "_".join([name, str(c)])
                else:
                    fname = col

                plt.savefig("plots/{}.png".format(fname))

    else:
        plt.clf()
        cs = 0

        anz = len(cols)
        for col in cols:
            if isinstance(col, str):
                cs += 1
                plt.subplot(1, anz, cs)
                df.boxplot(col, grid=False)

                if ylim:
                    plt.ylim(ymin=0)
            else:
                cs += 1
                plt.subplot(1, anz, cs)
                df.boxplot(col[0], grid=False)

                plt.ylim(ymax=col[1]*1.01)

                if ylim:
                    plt.ylim(ymin=0)

        if draw:
            plt.show()

        if name:
            fname = name
        else:
            fname = str(cols)[1:-2].replace("'", "")

        plt.savefig("plots/{}.png".format(fname))


def gen_graphs_misc():
    df.sort_values('DS', ascending=False)[
        ['DS']].plot.bar(grid=False, xlabel="Portal ID", ylabel="Anzahl Datensätze",
                         title="Datensätze pro Portal")
    plt.savefig("plots/{}.png".format("DS_Anzahl"))
    plt.clf()

    df["Portalsoftware"] = df[["Portalsoftware"]].replace([2, 3, 4], ["ckan", "arcgis", "dkan"])

    df.groupby("Portalsoftware").sum().plot.pie(y="Portal", title="Verteilung Portaltypen", autopct="%.0f pct",
                                                legend=False)
    plt.savefig("plots/{}.png".format("Portaltypen"))
    plt.clf()


def gen_graphs_ds_roh():
    get_titel_laenge_ds()

    # Kontakte
    get_graphs([["DS_Autor_valide_Anteil", "DS_Verwalter_valide_Anteil"]],
               name="DS_Kontakte")

    # Misc
    get_graphs([["DS_URL_Anteil", "DS_geo_Anteil"]],
               name="DS_Misc")

    # DS Datum
    get_graphs([["DS_Erstelldatum_Anteil", "DS_Updatedatum_Anteil", "Updatedatum_ung_Erstelldatum_Anteil"]],
               name="DS_Datum", rot=5)

    # DS Tags
    get_graphs(["DS_mit_Tags_Anteil", "Tags_pro_DS_Durchschnitt"],
               name="DS_Tags", ylim=True)

    # DS Gruppen
    get_graphs(["DS_mit_Gruppen_Anteil", "Gruppen_pro_DS_Durchschnitt"],
               name="DS_Gruppen", sub=True)

    # DS Lizenzen
    get_graphs(["Lizenzen_einz", ["DS_mit_Lizenz_Anteil", "DS_mit_Lizenz_offen_Anteil"]],
               name="DS_Lizenzen")

    # Roh Generell
    get_graphs(["Roh_pro_DS"],
               name="Roh_pro_DS", ylim=True)

    # Roh Links
    get_graphs([["online_Anteil", "Link_intern_Anteil"]],
               name="Roh_Links")

    # Roh Titel Beschr
    get_graphs([["Name_Anteil", "DS_Name_einz_Anteil", "Beschreibung_Roh_Anteil"]],
               name="Roh_Titel_Beschreibung_Anteil")
    get_graphs(["Name_einz_Laenge", "Beschreibung_Roh_Laenge"],
               name="Roh_Titel_Beschreibung_Laenge", sub=True)

    # Roh Datum
    get_graphs([["Roh_Erstelldatum_Anteil", "Roh_Updatedatum_Anteil", "Roh_Updatedatum_ung_Erstelldatum_Anteil"]],
               name="Roh_Datum", rot=5)

    # Roh Dateityp
    get_graphs([["Dateityp_einz", "DateitypReal_einz"],
                ["Dateityp_gegeben_Anteil", "DateitypReal_gegeben_Anteil"],
                "DateitypReal_einz_DS_Durchschnitt",
                ["Roh_ML_Anteil", "Roh_offen_Anteil"],
                "Roh_validierbar_Anteil"],
               name="Roh_Dateityp")

    # Roh valide
    get_graphs([["valid_0_Anteil",
                 "valid_1_Anteil",
                 "valid_2_Anteil",
                 "valid_3_Anteil",
                 "valid_4_Anteil",
                 "valid_5_Anteil"]],
               name="Roh_valide", rot=10)

    # Roh Fehler
    get_graphs(["Fehler_Durchschnitt", "Fehler_validierbar_Durchschnitt", "Fehler_pro_Roh_Durchschnitt"],
               name="Roh_Fehler_Durchschnitte", sub=True, draw=True)
    get_graphs([["Roh_Fehler_Zelle_Anteil",
                 "Roh_Fehler_Reihe_Anteil",
                 "Roh_Fehler_Label_Anteil"],
                ["Fehler_Zelle_Anteil",
                 "Fehler_Reihe_Anteil",
                 "Fehler_Label_Anteil"]
                ],
               name="Roh_Fehler_R_Anteile")

    # Roh Dategroeße
    get_graphs(["Dateigroesse_Durchschnitt", "Dateigroesse_min", "Dateigroesse_max", "Dateigroesse_Summe"],
               name="Roh_Dateigröße", sub=True, rot=0, draw=True)


def gen_graphs_framew():
    # Genauigkeit
    # get_graphs([("gen_titel", 4),
    #             ("gen_beschreibung", 3),
    #             ("gen_tags", 1),
    #             ("gen_geodaten", 1),
    #             ("gen_metaValidität", 1),
    #             ("gen_score", 10)],
    #            name="Framework_Genauigkeit", sub=True, draw=True, ylim=True)
    #
    # # Vollständigkeit
    # get_graphs([("vollst_gewVollst", 7),
    #             ("vollst_rohZelle", 1),
    #             ("vollst_rohReihe", 1),
    #             ("vollst_rohLabel", 1),
    #             ("vollst_score", 10)],
    #            name="Framework_Vollständigkeit", sub=True, draw=True, ylim=True)
    #
    # # Aktualität
    # get_graphs([("akt_updates", 3),
    #             ("akt_erstellt", 3),
    #             ("akt_neueDaten", 2),
    #             ("akt_alterDaten", 2),
    #             ("akt_score", 10)],
    #            name="Framework_Aktualität", sub=True, draw=True, ylim=True)
    #
    # # Abrufbarkeit
    # get_graphs([("abr_linkOnline", 9),
    #             ("abr_linkIntern", 1),
    #             ("abr_score", 10)],
    #            name="Framework_Abrufbarkeit", sub=True, draw=True, ylim=True)
    #
    # # Offenheit
    # get_graphs([("off_dfML", 4),
    #             ("off_dfOffen", 2),
    #             ("off_lizenzOffen", 4),
    #             ("off_score", 10)],
    #            name="Framework_Offenheit", sub=True, draw=True, ylim=True)
    #
    # # Kontaktierbarkeit
    # get_graphs([("kon_autorValide", 5),
    #             ("kon_verwalterValide", 5),
    #             ("kon_score", 10)],
    #            name="Framework_Kontaktierbarkeit", sub=True, draw=True, ylim=True)
    #
    # # Rückverfolgbarkeit
    # get_graphs([("rue_quelle", 10),
    #             ("rue_score", 10)],
    #            name="Framework_Rückverfolgbarkeit", sub=True, draw=True, ylim=True)
    #
    # # Validität
    # get_graphs([("val_rdLesbar", 5),
    #             ("val_rdValide", 5),
    #             ("val_score", 10)],
    #            name="Framework_Validität", sub=True, draw=True, ylim=True)
    #
    # # Diversität
    # get_graphs([("div_durchEndp", 2),
    #             ("div_stdevEndp", 1),
    #             ("div_durchDF", 2),
    #             ("div_stdevDF", 1)],
    #            name="Framework_Diversität_1", sub=True, draw=True, ylim=True)

    get_graphs([("div_durchTags", 2),
                ("div_stdevTags", 1),
                ("div_anteilOrg", 0.5),
                ("div_stdevOrg", 0.5),
                ("div_score", 10)],
               name="Framework_Diversität_2", sub=True, draw=True, ylim=True)


def get_graphs_framew_scores():
    # Genauigkeit
    df.sort_values('gen_score', ascending=False)[
        ['gen_titel', 'gen_beschreibung', "gen_tags", "gen_geodaten", "gen_metaValidität"]] \
        .plot.bar(stacked=True, grid=False, xlabel="Portal ID", ylabel="Gesamtbewertung", title="Übersicht Genauigkeit")
    plt.savefig("plots/{}.png".format("Framework_Genauigkeit_rank"))
    plt.clf()

    # Vollständigkeit
    df.sort_values('vollst_score', ascending=False)[
        ['vollst_gewVollst', 'vollst_rohZelle', "vollst_rohReihe", "vollst_rohLabel"]] \
        .plot.bar(stacked=True, grid=False, xlabel="Portal ID", ylabel="Gesamtbewertung",
                  title="Übersicht Vollständigkeit")
    plt.savefig("plots/{}.png".format("Framework_Vollständigkeit_rank"))
    plt.clf()

    # Aktualität
    df.sort_values('akt_score', ascending=False)[
        ['akt_updates', 'akt_erstellt', "akt_neueDaten", "akt_alterDaten"]] \
        .plot.bar(stacked=True, grid=False, xlabel="Portal ID", ylabel="Gesamtbewertung",
                  title="Übersicht Aktualität")
    plt.savefig("plots/{}.png".format("Framework_Aktualität_rank"))
    plt.clf()

    # Abrufbarkeit
    df.sort_values('abr_score', ascending=False)[
        ['abr_linkOnline', 'abr_linkIntern']] \
        .plot.bar(stacked=True, grid=False, xlabel="Portal ID", ylabel="Gesamtbewertung",
                  title="Übersicht Abrufbarkeit")
    plt.savefig("plots/{}.png".format("Framework_Abrufbarkeit_rank"))
    plt.clf()

    # Offenheit
    df.sort_values('off_score', ascending=False)[
        ['off_dfML', 'off_dfOffen', "off_lizenzOffen"]] \
        .plot.bar(stacked=True, grid=False, xlabel="Portal ID", ylabel="Gesamtbewertung",
                  title="Übersicht Offenheit")
    plt.savefig("plots/{}.png".format("Framework_Offenheit_rank"))
    plt.clf()

    # Kontaktierbarkeit
    df.sort_values('kon_score', ascending=False)[
        ['kon_autorValide', 'kon_verwalterValide']] \
        .plot.bar(stacked=True, grid=False, xlabel="Portal ID", ylabel="Gesamtbewertung",
                  title="Übersicht Kontaktierbarkeit")
    plt.savefig("plots/{}.png".format("Framework_Kontaktierbarkeit_rank"))
    plt.clf()

    # Rückverfolgbarkeit
    df.sort_values('rue_score', ascending=False)[
        ['rue_quelle']] \
        .plot.bar(stacked=True, grid=False, xlabel="Portal ID", ylabel="Gesamtbewertung",
                  title="Übersicht Rückverfolgbarkeit")
    plt.savefig("plots/{}.png".format("Framework_Rückverfolgbarkeit_rank"))
    plt.clf()

    # Validität
    df.sort_values('val_score', ascending=False)[
        ['val_rdLesbar', 'val_rdValide']] \
        .plot.bar(stacked=True, grid=False, xlabel="Portal ID", ylabel="Gesamtbewertung",
                  title="Übersicht Validität")
    plt.savefig("plots/{}.png".format("Framework_Validität_rank"))
    plt.clf()

    # Diversität
    df.sort_values('div_score', ascending=False)[
        ['div_durchEndp', 'div_stdevEndp', "div_durchDF", "div_stdevDF",
         "div_durchTags", "div_stdevTags", "div_anteilOrg", "div_stdevOrg"]] \
        .plot.bar(stacked=True, grid=False, xlabel="Portal ID", ylabel="Gesamtbewertung", title="Übersicht Diversität")
    plt.savefig("plots/{}.png".format("Framework_Diversität_rank"))
    plt.clf()

    # Gesamt
    df.sort_values('gesamt_score', ascending=False)[
        ['gen_gewScore', 'vollst_gewScore', "akt_gewScore", "abr_gewScore",
         "off_gewScore", "kon_gewScore", "rue_gewScore", "val_gewScore", "div_gewScore"]] \
        .plot.bar(stacked=True, grid=False, xlabel="Portal ID", ylabel="Gesamtbewertung (gew.)",
                  title="Übersicht Gesamtbewertung")
    plt.savefig("plots/{}.png".format("Framework_gesamt_rank"))
    plt.clf()

    # Portal Ebene
    df.sort_values('portalEbene_score', ascending=False)[
        ['portalEbene_neueDaten', 'portalEbene_durchEndp', "portalEbene_stdevEndp", "portalEbene_durchDF",
         "portalEbene_stdevDF", "portalEbene_durchTags", "portalEbene_stdevTags", "portalEbene_anteilOrg",
         "portalEbene_stdevOrg", "portalEbene_linkOnline"]] \
        .plot.bar(stacked=True, grid=False, xlabel="Portal ID", ylabel="Gesamtbewertung",
                  title="Übersicht Portal-Ebene")
    plt.savefig("plots/{}.png".format("Framework_portalebene_rank"))
    plt.clf()

    # Meta Ebene
    df.sort_values('metaEbene_score', ascending=False)[
        ['metaEbene_metaValidität', 'metaEbene_geodaten', "metaEbene_titel", "metaEbene_beschreibung",
         "metaEbene_tags", "metaEbene_gewVollst", "metaEbene_updates", "metaEbene_erstellt",
         "metaEbene_alterDaten", "metaEbene_linkIntern", "metaEbene_linkOnline", "metaEbene_lizenzOffen",
         "metaEbene_autorValide", "metaEbene_verwalterValide", "metaEbene_quelle"]] \
        .plot.bar(stacked=True, grid=False, xlabel="Portal ID", ylabel="Gesamtbewertung",
                  title="Übersicht Meta-Ebene")
    plt.savefig("plots/{}.png".format("Framework_metaebene_rank"))
    plt.clf()

    # Roh Ebene
    df.sort_values('rohEbene_score', ascending=False)[
        ["rohEbene_rohZelle", "rohEbene_rohReihe", "rohEbene_rohLabel", "rohEbene_dfML", "rohEbene_dfOffen",
         "rohEbene_rdLesbar", "rohEbene_rdValide"]] \
        .plot.bar(stacked=True, grid=False, xlabel="Portal ID", ylabel="Gesamtbewertung",
                  title="Übersicht Roh-Ebene")
    plt.savefig("plots/{}.png".format("Framework_rohebene_rank"))
    plt.clf()

    # Gesamt Ebenen
    df.sort_values('gesamt_score_ebenen', ascending=False)[
        ['rohEbene_score', 'metaEbene_score', "portalEbene_score"]] \
        .plot.bar(stacked=True, grid=False, xlabel="Portal ID", ylabel="Gesamtbewertung",
                  title="Übersicht Gesamtbewertung n. Ebenen")
    plt.savefig("plots/{}.png".format("Framework_gesamt_Ebenen_rank"))
    plt.clf()


if __name__ == '__main__':
    df = pd.read_csv("results.csv", dtype=np.float32, encoding="iso-8859-1")
    df["Portal"] = df["Portal"].astype(int)
    df["DS"] = df["DS"].astype(int)

    # gen_graphs_misc()
    # gen_graphs_ds_roh()
    # gen_graphs_framew()
    # get_graphs_framew_scores()
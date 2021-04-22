import frictionless
import goodtables


def get_valid(file):
    """
    Validiert eine Rohdatendatei, falls diese die Kriterien erfüllt und liefert ein standardisiertes Ergebnis
    :param file: Name der Rohdatendatei (String)
    :return: Ein Dictionary mit den Validierungsergebnissen
    """
    ftype = file.split(".")[-1].lower()

    try:
        # frictionless handles everything but JSON better.
        if ftype in ["csv", "xls", "xlsx", "ods"]:
            result = frictionless.validate(file)
            result = reformat_result(result, "fric")

        # JSON must be done with goodtables for now.
        elif ftype in ["json"]:
            result = goodtables.validate(file, row_limit=10000)
            result = reformat_result(result, "good")

        else:
            result = False

    except Exception:
        result = {"valide": 3,
                  "fehler": None,
                  "anzahlFehler": None
                  }

    return result


def reformat_result(result, lib):
    """
    Überführt die verschiedenen Ergebnis-Formate der Bibliotheken in einen Standard.
    :param result: Validierungsergebnisse (Dictionary)
    :param lib: Verwendete Bibliothek (String)
    :return: Eine standardisierte Form des Ergebnisses (Dictionary)
    """
    new_result = {
        "valide": 0,
        "fehler": [],
        "anzahlFehler": None,
    }

    # valide transkribieren
    if result["valid"]:
        new_result["valide"] = 1

    # Frictionless hat manchmal ein unterschiedliches Ergebnisformat. Warum?
    if "tasks" in result:
        fehler_liste = result["tasks"][0]["errors"]
    elif "tables" in  result:
        fehler_liste = result["tables"][0]["errors"]
    else:
        fehler_liste = []

    # Unterschied frictionless / goodtables Ergebnisse
    if lib == "fric":
        new_result["fehler"] = [{
            "rohDatensatzID": "dummy",
            "fehlerCode": fehler["code"],
            "fehlerNachricht": fehler["message"],
            "fehlerTags": fehler["tags"],
            "fehlerExtras": gen_extras(fehler)
        }
            for fehler in fehler_liste
        ]
    else:
        new_result["fehler"] = [{
            "rohDatensatzID": "dummy",
            "fehlerCode": fehler["code"],
            "fehlerNachricht": fehler["message"],
            "fehlerTags": None,
            "fehlerExtras": None
        }
            for fehler in fehler_liste
        ]

    # Fehleranzahl für einfachere Statistik angeben
    new_result["anzahlFehler"] = len(new_result["fehler"])

    return new_result


def gen_extras(fehler):
    """
    Fügt noch nicht genutzte Informationen in ein 'Extra' Feld für jeden Fehler.
    :param fehler: Eine Fehler-Information der Validierung
    :return: Ein String mit allen bisher nicht genutzten Informationen im Dictionary-Format.
    """
    felder = ["fieldName, fieldNumber, fieldPosition, labels, cells, rowNumber, rowPosition, notes"]
    extras = {}

    for feld in felder:
        if feld in fehler:
            extras[feld] = fehler[feld]

    return str(extras)

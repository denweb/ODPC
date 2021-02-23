import frictionless
import goodtables
import json
from pprint import pprint

# Todo: Link aus DB ziehen, Datei herunterladen & mit entsprechenden Infos weiterverarbeiten.
file = "opendata_v.csv"


# Todo: Ergebnis-Format anpassen für jeweils verwendete Bibliothek
def get_valid(file):
    ftype = file.split(".")[-1].lower()

    try:
        # frictionless handles everything but JSON better.
        if ftype in ["csv", "xlx", "xlsx", "ods"]:
            result = frictionless.validate(file)
            result = reformat_result(result, 1)

        # JSON must be done with goodtables for now.
        elif ftype in ["json"]:
            result = goodtables.validate(file, row_limit=10000)
            result = reformat_result(result, 2)

        else:
            result = False
    except Exception:
        result = {"valid": 3,
                  "fehler": [],
                  "anzahlFehler": 0
                  }

    return result


def reformat_result(result, case):
    new_result = {}

    # valide transkribieren
    if result["valid"]:
        new_result["valide"] = 1
    else:
        new_result["valide"] = 0

    # frictionless-format
    if case == 1:
        new_result["fehler"] = [{
            "rohDatensatzID": "dummy",
            "fehlerCode": fehler["code"],
            "fehlerNachricht": fehler["message"],
            "fehlerTags": fehler["tags"],
            "fehlerExtras": gen_extras(fehler)
        }
                                for fehler in result["tables"][0]["errors"]
                                ]

    # goodtables format
    else:
        new_result["fehler"] = [{
            "rohDatensatzID": "dummy",
            "fehlerCode": fehler["code"],
            "fehlerNachricht": fehler["message"],
            "fehlerTags": False,
            "fehlerExtras": False
        }
            for fehler in result["tables"][0]["errors"]
        ]

    # Fehleranzahl für einfachere Statistik angeben
    new_result["anzahlFehler"] = len(new_result["fehler"])

    return new_result


def gen_extras(fehler):
    felder = ["fieldName, fieldNumber, fieldPosition, labels, cells, rowNumber, rowPosition, notes"]
    extras = {}

    for feld in felder:
        if feld in fehler:
            extras[feld] = fehler[feld]

    return str(extras)


#pprint(get_valid(file))
#print(json.dumps(get_valid(file)))
# Todo: Ergebnis in DB speichern

#frictionless works for all formats except JSON...
#It depicts JSON as JSON, when the ending is given in caps. But
#Goodtables mag auch den geojson nicht.
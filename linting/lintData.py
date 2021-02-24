import frictionless
import goodtables
import json
from pprint import pprint


def get_valid(file):
    ftype = file.split(".")[-1].lower()

    try:
        # frictionless handles everything but JSON better.
        if ftype in ["csv", "xls", "xlsx", "ods"]:
            result = frictionless.validate(file)
            result = reformat_result(result, ftype)

        # JSON must be done with goodtables for now.
        elif ftype in ["json"]:
            result = goodtables.validate(file, row_limit=10000)
            result = reformat_result(result, ftype)

        else:
            result = False
    except Exception:
        result = {"valide": 3,
                  "fehler": [],
                  "anzahlFehler": 0
                  }

    return result


def reformat_result(result, ftype):
    new_result = {}

    # valide transkribieren
    if result["valid"]:
        new_result["valide"] = 1
    else:
        new_result["valide"] = 0

    # frictionless-format - unterschiede zwischen Ergebnisformaten
    if ftype in ["csv", "ods"]:
        new_result["fehler"] = [{
            "rohDatensatzID": "dummy",
            "fehlerCode": fehler["code"],
            "fehlerNachricht": fehler["message"],
            "fehlerTags": fehler["tags"],
            "fehlerExtras": gen_extras(fehler)
        }
                                for fehler in result["tables"][0]["errors"]
                                ]
    elif ftype in ["xls", "xlsx"]:
        new_result["fehler"] = [{
            "rohDatensatzID": "dummy",
            "fehlerCode": fehler["code"],
            "fehlerNachricht": fehler["message"],
            "fehlerTags": fehler["tags"],
            "fehlerExtras": gen_extras(fehler)
        }
                                for fehler in result["tasks"][0]["errors"]
                                ]

    # goodtables format
    else:
        new_result["fehler"] = [{
            "rohDatensatzID": "dummy",
            "fehlerCode": fehler["code"],
            "fehlerNachricht": fehler["message"],
            "fehlerTags": None,
            "fehlerExtras": None
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

#file = "G_IV_1_m0409_H.xls"

#pprint(get_valid(file))
#print(json.dumps(get_valid(file)))

#frictionless works for all formats except JSON...
#It depicts JSON as JSON, when the ending is given in caps. But
#Goodtables mag auch den geojson nicht.
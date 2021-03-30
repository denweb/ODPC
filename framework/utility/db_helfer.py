from framework.utility.lizenzen import lizenzen
from framework.utility.dateiFormate import machine_readable, non_propr


def get_offene_lizenzen(db):
    db_liz = db.get_tables_dict("lizenz")

    offene_lizenzen_daten = "\t".join(lizenzen["daten"])
    ids = (2, 3, 6, 7, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22)
    print(offene_lizenzen_daten)

    liz_ids = set()
    for lizenz in db_liz:
        if any([lizenz["lizenzTitel"] in offene_lizenzen_daten,
                lizenz["lizenzUrl"] in offene_lizenzen_daten],
               lizenz["lizenzID"]):
            liz_ids.add(lizenz["lizenzID"])

    return liz_ids


def get_dateiformat_ids(db):
    db_df = db.get_tables_dict("dateiTyp")

    res = {
        "dateiformate_mr": {df["dateiTypID"] for df in db_df for df_mr in machine_readable if df_mr in df["dateiTyp"].lower()},
        "dateiformate_np": {df["dateiTypID"] for df in db_df for df_np in non_propr if df_np in df["dateiTyp"].lower()}
    }

    return res


def gen_sql(framework_dict, name):
    keys = ", ".join("".join(["'", key, "'"]) for key in framework_dict.keys())
    values = ", ".join([str(framework_dict[key]) for key in framework_dict.keys()])

    sql = "INSERT INTO {0} " \
          "({1}) " \
          "VALUES ({2})".format(name, keys, values)

    return sql

from framework.utility.dateiFormate import machine_readable, non_propr


def get_dateiformat_ids(db):
    """
    Funktion um die die IDs der offenen und maschinenlesbaren Dateitypen in der Datenbank zu erhalten.
    :param db: Die Verbindung zur Datenbank (DBConnection Instanz)
    :return: Ein Dictionary mit den IDs der oben beschriebenen Dateitypen in der Datenabnk.
    """
    db_df = db.get_tables_dict("dateiTyp")

    res = {
        "dateiformate_mr": {df["dateiTypID"] for df in db_df for df_mr in machine_readable if
                            df_mr in df["dateiTyp"].lower()},
        "dateiformate_np": {df["dateiTypID"] for df in db_df for df_np in non_propr if df_np in df["dateiTyp"].lower()}
    }

    return res


def gen_sql(framework_dict, name):
    """
    Generiert den SQL-Code zum Einfügen der Dimensionen in die jeweiligen Tabellen der framework.db
    :param framework_dict: Ein Dictionary mit den Werten zum Einfügen
    :param name: Der Name der Tabelle (String)
    :return: Der SQL-Code als String.
    """
    keys = ", ".join("".join(["'", key, "'"]) for key in framework_dict.keys())
    values = ", ".join([str(framework_dict[key]) for key in framework_dict.keys()])

    sql = "INSERT INTO {0} " \
          "({1}) " \
          "VALUES ({2})".format(name, keys, values)

    return sql

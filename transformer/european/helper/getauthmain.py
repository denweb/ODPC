def get_authmain(dataitem, type):
    result = "N/A"

    if type == "author":
        if dataitem["publisher"] is not None:
            if "name" in dataitem["publisher"]:
                if all([dataitem["publisher"]["name"] is not None,
                        dataitem["publisher"]["name"] != "",
                        dataitem["publisher"]["name"] != " "]):
                    result = dataitem["publisher"]["name"]
        else:
            result = "N/A"

    elif type == "maintainer":
        if dataitem["contact_points"] is not None:
            if "name" in dataitem["contact_points"]:
                if all([dataitem["contact_points"]["name"] is not None,
                        dataitem["contact_points"]["name"] != "",
                        dataitem["contact_points"]["name"] != " "]):
                    result = dataitem["contact_points"]["name"]
        else:
            result = "N/A"

    return result

from transformer.helper.transformmail import transform_mail


def get_mail(dataitem, type):
    result = "N/A"

    if type == "author":
        if dataitem["publisher"] is not None:
            if "name" in dataitem["publisher"]:
                result = transform_mail(dataitem["publisher"]["name"])
        else:
            result = "N/A"

    elif type == "maintainer":
        if dataitem["contact_points"] is not None:
            if "name" in dataitem["contact_points"]:
                result = transform_mail(dataitem["contact_points"]["email"])
        else:
            result = "N/A"

    return result

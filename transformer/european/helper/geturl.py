def get_url(organization):
    result = "N/A"

    if "publisher" in organization:
        if organization["publisher"] is not None:
            if "email" in organization["publisher"]:
                if any([
                    organization["publisher"]["email"] is not None,
                    organization["publisher"]["email"] != "",
                    organization["publisher"]["email"] != " "
                ]):
                    result = organization["publisher"]["email"]

    return result


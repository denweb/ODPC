import uuid


def get_id(url_string):
    if "/" in url_string:
        split = url_string.split("/")
        return split[-1]
    else:
        return str(uuid.uuid4())
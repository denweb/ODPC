def get_domain(url_raw):
    try:
        url_split = url_raw.split("/")

        if ":" in url_split[2]:
            split_2 = url_split[2].split(":")[0]
            new_url = "".join([url_split[0], url_split[1], "//", split_2])
        else:
            new_url = "".join([url_split[0], url_split[1], "//", url_split[2]])
    except:
        new_url = url_raw

    return new_url

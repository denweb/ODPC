def distribute(link, portal):
    if portal == "arcgis":
        # Todo: Pass to arcgis cralwer here
        pass
    elif portal == "ckan":
        # Todo: Pass to ckan crawler here
        pass
    elif portal == "socrata":
        # Todo: Pass to socrata crawler here
        pass
    elif portal == "european":
        # Todo: Pass to european crawler here
        pass
    else:
        print("Portal of uknown format: %s" % link)

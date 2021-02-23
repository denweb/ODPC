def transform_mail(mailstring):
    res = None
    if isinstance(mailstring, str):
        if mailstring.startswith("mailto:"):
            new_mail = mailstring[7:]
            if new_mail:
                res = new_mail
        elif mailstring == "":
            res = None
        elif mailstring == " ":
            res = None
        elif not mailstring:
            res = None
        else:
            res = mailstring

    return res

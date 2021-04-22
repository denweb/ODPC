import re


def remove_html_tags(text):
    """
    Entfernt HTML-Reste aus einem String
    :param text: Der zu reinigende String
    :return: Der bereinigte String
    """
    res = None
    if text:
        clean = re.compile('<.*?>')
        res = re.sub(clean, ' ', text)

    return res

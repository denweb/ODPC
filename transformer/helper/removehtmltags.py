import re


def remove_html_tags(text):
    """Remove html tags from a string"""
    res = None
    if text:
        clean = re.compile('<.*?>')
        res = re.sub(clean, ' ', text)

    return res

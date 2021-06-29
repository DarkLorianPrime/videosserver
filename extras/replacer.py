import re


def replacer(text):
    text = re.sub(r"[$|@|&|`|'| |:|.|,|;|/|\|~|%|$|#|@|!|^|*|(|)|{|}]",  '_', text)
    return text

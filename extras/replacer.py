import re


def replacer(text):
    text = re.sub(r"^\w\d_",  '_', text)
    return text

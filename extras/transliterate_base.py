from transliterate.base import TranslitLanguagePack


def get_translation() -> dict:
    """
    художественный фильм - взято без спросу.
    feat. Andrey Cherabaev
    """
    russian_layout = """АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШOЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя"""
    english_layout = """F<DULT~:PBQRKVYJGHCNEA{WXIO}SM">Zf,dult`;pbqrkvyjghcnea[wxio]sm'.z"""
    return ''.maketrans(english_layout + russian_layout, russian_layout + english_layout)


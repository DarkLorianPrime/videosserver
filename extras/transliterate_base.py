from transliterate.base import TranslitLanguagePack


class HTMLLanguagePack(TranslitLanguagePack):
    language_code = "HTML"
    language_name = "HTML"
    mapping = (
        u"'`[()]абвгдежзийклмнопрстуфхцчшщъыьэюя",
        u"______abvgdez",
    )


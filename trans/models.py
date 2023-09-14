import json
import locale
#locale.setlocale(locale.LC_ALL, 'fi_FI.UTF-8')

with open('trans/models.json') as f:
    model_info = json.load(f)
    model_info.sort(key=lambda info: locale.strxfrm(info['label']))
    available_translations = set()

    for model in model_info:
        tr = model['value']
        available_translations.add(tr)

def model_exists(frm, to):
    return f'{frm} {to}' in available_translations

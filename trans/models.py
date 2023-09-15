import json

with open('trans/models.json') as f:
    model_info = json.load(f)
    available_translations = set()

    for model in model_info:
        tr = model['value']
        available_translations.add(tr)

def model_exists(frm, to):
    return f'{frm} {to}' in available_translations


def value_for_label(label):
    for info in model_info:
        if info['label'] == label:
            return info['value']
    return None

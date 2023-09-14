"""Tulostaa kaikki mahdolliset lähdekieli–kohdekieli-parit json-muodossa annettuun tiedostoon.
"""

import json
import re
import sys

from huggingface_hub import list_models
from langcodes import Language

def language_name(code):
    return Language.get(code).display_name('fi')


if len(sys.argv) != 2:
    print(__doc__)
    sys.exit(f'Käyttö: {sys.argv[0]} <tiedosto>')


model_ids = [ x.modelId
              for x in list_models()
              if re.match(r'^Helsinki-NLP/opus-mt-[a-z]{2,3}-[a-z]{2,3}$', x.modelId)
            ]

model_list = []
for model_id in model_ids:
    frm, to = model_id.strip().replace('Helsinki-NLP/opus-mt-', '').split('-')
    entry = {
        'label': language_name(frm) + ' → ' + language_name(to),
        'value': frm + ' ' + to
    }
    model_list.append(entry)



with open(sys.argv[1], 'w') as f:
    json.dump(model_list, f, indent=2)
    print(f'Tulostettiin {len(model_list)} mallia')

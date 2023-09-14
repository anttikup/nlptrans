import os
import requests
import sys

from trans.models import model_exists

API_TOKEN = os.environ['API_TOKEN']

headers = {'Authorization': 'Bearer ' + API_TOKEN}

def get_url(frm, to):
    if not model_exists(frm, to):
        raise Exception(f'Translation from {frm} to {to} is not available')

    return f'https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-{frm}-{to}'


def query(url, payload):
    response = requests.post(url, headers=headers, json=payload)
    return response.json()


def get_error_message(output):
    if 'error' in output:
        msg = output['error']
        if msg.endswith('is currently loading'):
            msg = msg.replace('Model', 'Mallia').replace('is currently loading', 'ladataan vielä.')

        if 'estimated_time' in output:
            msg = msg + ' Yritä uudelleen noin ' + str(round(output['estimated_time'])) + ' sekunnin päästä.'
        raise Exception(msg)
    else:
        raise Exception(str(output))


def translate(frm, to, texts):
    output = query(get_url(frm, to), {
	'inputs': texts,
    })

    if type(output) != list:
        raise Exception(get_error_message(output))

    return [ paragraph['translation_text'] for paragraph in output ]




if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(f'Käyttö: {sys.argv[0]} <mistä> <mihin>')

    frm = sys.argv[1]
    to = sys.argv[2]

    print('Anna teksti ja paina Ctrl-D: ')
    text = sys.stdin.read()

    print('━' * 80)
    output = translate(frm, to, text.split('\n\n'))

    for paragraph in output:
        print(paragraph)
        if paragraph != output[-1]:
            print()

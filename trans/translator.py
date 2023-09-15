import os
import requests
import sys
import time

from trans.models import model_exists

API_TOKEN = os.environ['API_TOKEN']

headers = {'Authorization': 'Bearer ' + API_TOKEN}

class NotReadyException(Exception):
    def __init__(self, message, time):
        super().__init__(message)
        self.time = time

def get_url(frm, to):
    if not model_exists(frm, to):
        raise Exception(f'Translation from {frm} to {to} is not available')

    return f'https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-{frm}-{to}'


def query(url, payload):
    response = requests.post(url, headers=headers, json=payload)
    return response.json()


def raise_error(output):
    if 'error' in output:
        msg = output['error']
        if msg.endswith('is currently loading') and 'estimated_time' in output:
            raise NotReadyException(msg, output['estimated_time'])
        else:
            raise Exception(msg)
    else:
        raise Exception(str(output))


def translate(frm, to, texts):
    output = query(get_url(frm, to), {
	'inputs': texts,
    })

    if type(output) != list:
        try:
            raise_error(output)
        except NotReadyException as err:
            time.sleep(err.time)
            output = query(get_url(frm, to), {
	        'inputs': texts,
            })


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

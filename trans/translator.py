import os
import requests
import sys

API_TOKEN = os.environ['API_TOKEN']

API_URLs = {
        'en fi': "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-fi",
        'fi en': "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-fi-en",
}

headers = {"Authorization": "Bearer " + API_TOKEN}

def query(url, payload):
	response = requests.post(url, headers=headers, json=payload)
	return response.json()

def translate(frm, to, texts):
    output = query(API_URLs[f'{frm} {to}'], {
	"inputs": texts,
    })

    if type(output) != list:
        if 'error' in output:
            msg = output["error"]
            if 'estimated_time' in output:
                msg = msg + '; Estimated loading time: ' + str(output['estimated_time']) + " s"
            raise Exception(msg)
        else:
            raise Exception(repr(output))

    return [ paragraph['translation_text'] for paragraph in output ]




if __name__ == "__main__":
    print(" Valmis")

    print("\b"*len("Ladataan...") + "Anna teksti ja paina Ctrl-D: ")
    text = sys.stdin.read()

    print("━" * 80)
    output = translate(text.split("\n\n"))

    for paragraph in output:
        print(paragraph)
        if paragraph != output[-1]:
            print()

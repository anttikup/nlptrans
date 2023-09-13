import os
import requests
import sys

API_TOKEN = os.environ['API_TOKEN']

API_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-fi"
headers = {"Authorization": "Bearer " + API_TOKEN}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def translate(texts):
    output = query({
	"inputs": texts,
    })

    if type(output) != list:
        return f'ERROR: {output}'

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

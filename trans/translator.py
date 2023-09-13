import os
import requests
import sys

API_TOKEN = os.environ['API_TOKEN']

API_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-fi"
headers = {"Authorization": "Bearer " + API_TOKEN}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def translate(text):
    output = query({
	"inputs": text.split("\n\n"),
    })

    return [ block['translation_text'] for block in output ]



if __name__ == "__main__":
    print(" Valmis")

    print("\b"*len("Ladataan...") + "Anna teksti ja paina Ctrl-D: ")
    text = sys.stdin.read()

    print("━" * 80)
    blocks = translate(text)
    print(blocks)
    for block in blocks:
        print(block)
        if block != blocks[-1]:
            print()

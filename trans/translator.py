print("Ladataan malli...", end="", flush=True)

from transformers import pipeline

pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-en-fi")
print(" Valmis")


def translate(text):
    result = pipe(text.split("\n\n"))
    return [ block['translation_text'] for block in result ]


if __name__ == "__main__":
    import sys

    print("\b"*len("Ladataan...") + "Anna teksti ja paina Ctrl-D: ")
    text = sys.stdin.read()

    print("━" * 80)
    blocks = translate(text)
    for block in blocks:
        print(block)
        if block != blocks[-1]:
            print()

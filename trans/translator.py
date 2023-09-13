from transformers import pipeline

pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-en-fi")


def translate(text):
    result = pipe(text)
    return result[0]['translation_text']

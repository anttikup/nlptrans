import os

from flask import Flask, render_template, request, flash, jsonify
from flask_oojsui import build_static_blueprint


import trans.translator
from trans.models import model_info, value_for_label


app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY=os.environ['SECRET_KEY'],
)

# Adds static assets for OOJS-UI to path
app.register_blueprint(build_static_blueprint("oojsui", __name__))

@app.route('/', methods=('GET',))
def root():
    text = ""
    translation = ""

    return render_template('index.html', text=text, translation=translation)


@app.route('/lookup', methods=('GET',))
def lookup():
    text = request.args.get('text')
    return jsonify([
        info for info in model_info if text in info['label']
    ])

@app.route('/translate', methods=('POST',))
def translate():
    text = request.form['text']
    model = request.form['language']
    value = value_for_label(model)
    if not value:
        return {
            'error': f'Mallia ”{model}” ei löydy'
        };

    frm, to = value.split(' ')

    try:
        translation = translator.translate(frm, to, text.split("\n\n"))
    except Exception as err:
        return {
            'error':  str(err)
        };

    return {
        'text': "\n\n".join(translation)
    }

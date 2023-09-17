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
print("X:", app.url_map)

@app.route('/', methods=('GET', 'POST'))
def root():
    text = ""
    translation = ""

    if request.method == 'POST':
        text = request.form['text']
        label = request.form['language']
        value = value_for_label(label)
        if value == None:
            flash(f'Virhe: Mallia {label} ei löydy')
        else:
            frm, to = value.split(" ")

            try:
                translation = translator.translate(frm, to, text.split("\r\n\r\n"))
            except Exception as err:
                flash(f'Virhe: {str(err)}')

    return render_template('index.html', text=text, translation=translation, models=model_info)


@app.route('/lookup', methods=('GET',))
def lookup():
    text = request.args.get('text')

    print("looking for:", text)
    return jsonify([
        info for info in model_info if text in info['label']
    ])

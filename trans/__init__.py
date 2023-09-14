from flask import Flask, render_template, request, flash

import trans.translator
from trans.models import model_info

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
)

@app.route('/', methods=('GET', 'POST'))
def hello():
    text = ""
    translation = ""

    if request.method == 'POST':
        text = request.form['text']
        frm, to = request.form['language'].split(" ")

        error = None

        try:
            translation = translator.translate(frm, to, text.split("\r\n\r\n"))
        except Exception as err:
            flash(f'Virhe: {str(err)}')

    return render_template('index.html', text=text, translation=translation, models=model_info)

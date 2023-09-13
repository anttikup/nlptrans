from flask import Flask, render_template, request, flash

import trans.translator

app = Flask(__name__)


@app.route('/', methods=('GET', 'POST'))
def hello():
    text = ""
    if request.method == 'POST':
        text = request.form['text']
        error = None

        if error is not None:
            flash(error)

        translation = translator.translate(text)


    return render_template('index.html', text=text, translation=translation)

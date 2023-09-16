from flask import Flask, render_template, request, flash

import trans.translator
from trans.models import model_info, value_for_label

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY=os.environ['SECRET_KEY'],
)

@app.route('/', methods=('GET', 'POST'))
def index():
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

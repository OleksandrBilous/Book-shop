from flask import render_template
from flask_logic import app

@app.route("/")
def main_page():
    return render_template('index.html')

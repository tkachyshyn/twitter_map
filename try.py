from fastapi import FastAPI
from flask import request, Flask, render_template
import flask
from twitter_map import create_map

app = flask.Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/', methods=['GET', 'POST'])
def my_form_post():
    if request.method == "POST":
        account = str(request.form['nick'])
        create_map(account)
        return render_template('twitter_map.html')

if __name__ == "__main__":
    app.run(debug=True)
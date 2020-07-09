from os import environ
from flask import Flask
import app


app = Flask(__name__)

@app.route("/")
def home():
    app.tweet()
    return "Tweeting a GOT Quote..."

app.run(host= '0.0.0.0', port=environ.get('PORT'))

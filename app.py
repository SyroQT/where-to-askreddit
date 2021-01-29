import os
import json

import pickle
from cleantext import clean
from flask import Flask, request, render_template, url_for

app = Flask(__name__)

with open("model.pkl", "rb") as handle:
    model = pickle.load(handle)


def __process(title, content):
    """Process data and cleans it for prediction"""
    features = []
    if len(title) == len(content):
        for t, c in zip(title, content):
            features.append(
                clean(
                    t + c,
                    no_line_breaks=True,
                    no_urls=True,
                    no_emails=True,
                    no_phone_numbers=True,
                    no_numbers=True,
                    no_digits=True,
                    no_currency_symbols=True,
                    no_punct=True,
                )
            )
        return features
    else:
        raise TypeError


def __predict(data):
    return model.predict(data)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        if request.form:
            title = [request.form["title"]]
            content = [request.form["content"]]
        else:
            try:
                data = json.loads(request.data)["data"]
                title = data["title"]
                content = data["content"]
            except:
                return json.dumps({"error": "Bad data format"}), 400

        try:
            features = __process(title, content)
        except:
            return json.dumps({"error": "Error while parsing the data"}), 400

        try:
            prediction = __predict(features)
        except:
            return json.dumps({"error": "Prediction failed"}), 500

        if request.form:
            return render_template("index.html", prediction=prediction[0])
        else:
            return json.dumps({"predictions": prediction.tolist()})


@app.route("/info", methods=["GET", "POST"])
def info():
    """Return last 10 predictions made"""
    pass


if __name__ == "__main__":
    app.run()
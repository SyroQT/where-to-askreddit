import os
import json
from datetime import datetime

import pickle
import psycopg2
from cleantext import clean
from flask import Flask, request, render_template, url_for

app = Flask(__name__)

with open("model.pkl", "rb") as handle:
    model = pickle.load(handle)


def __process(title: str, content: str) -> list:
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


def __predict(data: list) -> list:
    return model.predict(data)


def __connect() -> tuple:
    """Return connection and cursor to the database"""
    host = os.getenv("host")
    database = os.getenv("database")
    user = os.getenv("user")
    port = os.getenv("port")
    password = os.getenv("password")

    conn = psycopg2.connect(
        host=host, database=database, user=user, port=port, password=password
    )
    cur = conn.cursor()
    return conn, cur


@app.route("/", methods=["GET", "POST"])
def index():
    """Index of wepbage and POST API"""
    # Logic for GET
    if request.method == "GET":
        return render_template("index.html")

    # Logic for POST
    if request.method == "POST":
        if request.form:  # FORM handling
            title = [request.form["title"]]
            content = [request.form["content"]]
        else:  # API handling
            try:
                data = json.loads(request.data)["data"]
                title = data["title"]
                content = data["content"]
            except:
                return json.dumps({"error": "Bad data format"}), 400

        # Preprocessing
        try:
            features = __process(title, content)
        except:
            return json.dumps({"error": "Error while parsing the data"}), 400
        # Prediction
        try:
            prediction = __predict(features)
        except:
            return json.dumps({"error": "Prediction failed"}), 500

        # Database logging
        try:
            conn, cur = __connect()
            dt = datetime.now()
            for feat, pred in zip(features, prediction):
                cur.execute(
                    f"""
                INSERT INTO history(features, prediction, date)
                VALUES (%s, %s, %s);
                """,
                    (feat, pred, dt),
                )
            conn.commit()
        except:
            print("Not inserted")

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
import requests

url = "http://127.0.0.1:5000/"


def test_get():
    resp = requests.get(url)
    assert resp.status_code == 200
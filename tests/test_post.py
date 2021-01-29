import json

import pytest
import requests

url = "http://127.0.0.1:5000/"

multi_data = {
    "data": {
        "title": [
            "whats your absolute favorite dipping sauce or condiment",
            "what is the biggest lesson you have learnt so far in life",
        ],
        "content": ["", ""],
    }
}
single_data = {
    "data": {
        "title": ["what if there was another continent in the pacific ocean"],
        "content": [""],
    }
}
bad_len = {
    "data": {
        "title": ["what if there was another continent in the pacific ocean"],
        "content": ["", ""],
    }
}
bad_format = {
    "data": {
        "title": ["what if there was another continent in the pacific ocean"],
        "content": ["", ""],
    }
}


def test_single():
    resp = requests.post(url, json.dumps(single_data))
    assert resp.status_code == 200


def test_multi():
    resp = requests.post(url, json.dumps(multi_data))
    assert resp.status_code == 200


def test_bad_format():
    resp = requests.post(url, json.dumps(bad_format))
    assert resp.status_code == 400


def test_error_wrong_len():
    resp = requests.post(url, json.dumps(bad_len))
    assert resp.status_code == 400

import requests


def test_model_chain():
    assert (
        requests.get("http://127.0.0.1:8000/model_chain/", json={"input": 5}).text
        == "12"
    )

import requests


def test_model_chain_name():
    assert (
        requests.get("http://127.0.0.1:8000/model_chain/name").text
        == '{"name":"model_chain_app"}'
    )


def test_model_chain():
    assert (
        requests.post(
            "http://127.0.0.1:8000/model_chain/ingress", json={"input": 5}
        ).text
        == '{"result":12}'
    )

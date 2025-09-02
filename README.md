# Model Chain Ray Serve Example

This repository demonstrates a simple model chaining pattern using [Ray Serve](https://docs.ray.io/en/latest/serve/index.html) and [FastAPI](https://fastapi.tiangolo.com/).

## Structure

```sh
.
├── README.md
├── pyproject.toml
├── src
│   ├── foo
│   │   └── __init__.py
│   └── model_chain
│       ├── __init__.py
│       ├── model_chain.py
│       └── run.py
├── tests
│   └── test_model_chain.py
└── uv.lock
```

## Usage

### Install dependencies

```bash
uv sync
```

### Start Ray Node

```bash
ray start --head --dashboard-host=0.0.0.0
```

### Deploy Serve Application/Model

```bash
uv run start_model_chain
```

### API Endpoints

- `POST /model_chain/ingress`:  

```python
assert (
    requests.post(
        "http://127.0.0.1:8000/model_chain/ingress", json={"input": 5}
    ).text
    == '{"result":12}'
)
```

- `GET /model_chain/name`:  

```python
assert (
    requests.get("http://127.0.0.1:8000/model_chain/name").text
    == '{"name":"model_chain_app"}'
)
```

### Stop/Remove the Deployed Ray Serve Application

```sh
uv run stop_model_chain
```

## Tests

```sh
$ uv run pytest   
======================================= test session starts =======================================
platform darwin -- Python 3.11.7, pytest-8.4.1, pluggy-1.6.0
rootdir: /Users/bensoorajmohan/Development/python-playground/foo
configfile: pyproject.toml
plugins: anyio-4.10.0
collected 2 items                                                                                 

tests/test_model_chain.py ..                                                                [100%]

======================================== 2 passed in 0.06s ========================================
```

## Issues

1. I am using pydantic models as inner classes. Defining it the standard way doesn't work when Ray tries to pickle the deployments. Need to find a better way to do this.

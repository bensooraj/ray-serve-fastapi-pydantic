from typing import Union
from pydantic import BaseModel
from starlette.requests import Request
from ray import serve
from ray.serve.handle import (
    DeploymentHandle,
    DeploymentResponse,
    DeploymentResponseGenerator,
)
from fastapi import FastAPI
from fastapi.responses import JSONResponse

RAY_SERVE_APPLICATION_NAME = "model_chain_app"

app = FastAPI()


@serve.deployment
class Adder:
    def __init__(self, increment: int):
        self._increment = increment

    def __call__(self, val: int) -> int:
        return val + self._increment


@serve.deployment
class Multiplier:
    def __init__(self, multiple: int):
        self._multiple = multiple

    def __call__(self, val: int) -> int:
        return val * self._multiple


@serve.deployment
@serve.ingress(app)
class Ingress:
    def __init__(self, adder: DeploymentHandle, multiplier: DeploymentHandle):
        self._adder = adder
        self._multiplier = multiplier

    class IngressNameResponse(BaseModel):
        name: str

    @app.get("/name", response_model=IngressNameResponse)
    def name(self) -> IngressNameResponse:
        return self.IngressNameResponse(name=RAY_SERVE_APPLICATION_NAME)

    class IngressRequest(BaseModel):
        input: int

    class IngressResponse(BaseModel):
        result: int

    @app.post("/ingress")
    async def add_and_multiply(self, payload: IngressRequest) -> IngressResponse:
        # input = (await request.json())["input"]
        input = payload.input
        adder_response: Union[DeploymentResponse, DeploymentResponseGenerator] = (
            self._adder.remote(input)
        )
        # Pass the adder response directly into the multiplier (no `await` needed).
        multiplier_response: Union[DeploymentResponse, DeploymentResponseGenerator] = (
            self._multiplier.remote(adder_response)
        )
        # `await` the final chained response.
        result = await multiplier_response
        return self.IngressResponse(result=result)

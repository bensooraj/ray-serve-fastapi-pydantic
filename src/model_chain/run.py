from .model_chain import RAY_SERVE_APPLICATION_NAME, Adder, Multiplier, Ingress
from ray import serve
from ray.serve import Application
from ray.serve.handle import (
    DeploymentHandle,
)


def serve_app() -> Application:
    app = Ingress.bind(  # type: ignore
        Adder.bind(increment=1),  # type: ignore
        Multiplier.bind(multiple=2),  # type: ignore
    )

    return app


def run():
    app = Ingress.bind(  # type: ignore
        Adder.bind(increment=1),  # type: ignore
        Multiplier.bind(multiple=2),  # type: ignore
    )

    try:
        handle: DeploymentHandle = serve.run(
            app, name=RAY_SERVE_APPLICATION_NAME, route_prefix="/model_chain"
        )

        print(f"""
deployment_name: {handle.deployment_name}
deployment_id: {handle.deployment_id}
app_name: {handle.app_name}
handle_id: {handle.handle_id}
""")

    except Exception as e:
        print(f"Error running Ray Serve app: {e}")

    finally:
        print("Ray Serve run attempt finished.")


def stop():
    serve.delete(RAY_SERVE_APPLICATION_NAME, True)

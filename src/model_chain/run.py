from .model_chain import (
    RAY_SERVE_APPLICATION_NAME,
    serve_app_builder,
)
from ray import serve
from ray.serve.handle import (
    DeploymentHandle,
)


def run():
    try:
        handle: DeploymentHandle = serve.run(
            serve_app_builder({}),
            name=RAY_SERVE_APPLICATION_NAME,
            route_prefix="/model_chain",
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

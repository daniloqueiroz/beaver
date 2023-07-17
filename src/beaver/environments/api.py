import logging
from enum import Enum
from uuid import uuid4

import docker  # type: ignore
from pydantic.main import BaseModel

from beaver import app
from beaver.server import Response, Success, Error

docker_client = docker.from_env()


class EnvironmentStatus(str, Enum):
    starting = "starting"
    running = "running"
    finalizing = "finalizing"
    gone = "gone"

    @staticmethod
    def from_container_status(status: str) -> "EnvironmentStatus":
        match status:
            case "running":
                return EnvironmentStatus.running
            case "restarting":
                return EnvironmentStatus.starting
            case "exited":
                return EnvironmentStatus.gone
        return EnvironmentStatus.gone


class Environment(BaseModel):
    name: str
    container_id: str | None = None
    status: EnvironmentStatus = EnvironmentStatus.starting


@app.get("/environments", tags=["environments"])
async def list_environments() -> Response[list[Environment]]:
    containers = docker_client.containers.list(filters={"label": "beaver.env=true"})
    logging.info("Found containers: %s", containers)
    environments = []
    for container in containers:
        env = Environment(
            name=container.labels["beaver.env.name"],
            container_id=container.id[:12],
            status=EnvironmentStatus.from_container_status(container.status),
        )
        environments.append(env)
    return Success(data=environments)


@app.post("/environments", status_code=201, tags=["environments"])
async def create_environment() -> Response[Environment]:
    env_name = generate_env_name()
    container = docker_client.containers.run(
        image="daniloqueiroz/beaver-base-env:latest",
        hostname=env_name,
        environment={
            "TS_AUTH_KEY": app.config.ts_api_key,
        },
        remove=True,
        detach=True,
        labels={
            "beaver.env": "true",  # this is a flag to identify the containers
            "beaver.env.name": env_name,
            "beaver.env.image": "daniloqueiroz/beaver-base-env:latest",
        },
        # TODO add the TS key id to the labels
    )
    env = Environment(name=env_name, container_id=container.id[:12])

    return Success(data=env)


@app.get("/environments/{env_name}", tags=["environments"])
async def get_environment(env_name: str) -> Response[Environment]:
    containers = docker_client.containers.list(
        filters={"label": f"beaver.env.name={env_name}"}
    )
    if len(containers) == 0:
        return Error(
            error="not_found",
            message=f"Environment {env_name} not found",
        )
    elif len(containers) > 1:
        return Error(
            error="internal_server_error",
            message=f"Found multiple containers with name {env_name}",
        )
    else:
        return Success(
            data=Environment(
                name=env_name,
                container_id=containers[0].id[:12],
                status=EnvironmentStatus.from_container_status(containers[0].status),
            )
        )


@app.delete("/environments/{env_name}", tags=["environments"], status_code=200)
async def delete_environment(env_name: str) -> Response[None]:
    containers = docker_client.containers.list(
        filters={"label": f"beaver.env.name={env_name}"}
    )
    if len(containers) == 0:
        return Error(
            error="not_found",
            message=f"Environment {env_name} not found",
        )
    elif len(containers) > 1:
        return Error(
            error="internal_server_error",
            message=f"Found multiple containers with name {env_name}",
        )
    else:
        containers[0].kill()
        return Success()


def generate_env_name() -> str:
    # generate a random and unique name for the environment in the format
    # beaver-<random string> and return it. The random string portion should be
    # unique enough to avoid collisions and short as possible
    suffix = uuid4().hex[:12]
    return f"beaver-{suffix}"

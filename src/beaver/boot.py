from fastapi import FastAPI

from beaver.configuration import Configuration


def init_app():
    app = FastAPI()
    # TODO change to get file name from env
    config = Configuration.from_file("config.yaml")
    app.config = config
    return app

from beaver import app
from beaver.configuration import Configuration
from beaver.server import Response, Success


@app.get("/configurations", tags=["admin"])
async def get_configurations() -> Response[Configuration]:
    return Success(data=app.config)


@app.put("/configurations", tags=["admin"])
async def update_configurations(config: Configuration) -> Response[Configuration]:
    app.config = config
    # TODO save to file
    return Success(data=app.config)

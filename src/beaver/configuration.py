from pydantic.main import BaseModel
from pydantic_yaml import parse_yaml_raw_as


class Configuration(BaseModel):
    ts_api_key: str = ""

    @staticmethod
    def from_file(path: str) -> "Configuration":
        with open(path, "r") as f:
            content = f.readline()
            if not content:
                content = "{}"
            return parse_yaml_raw_as(Configuration, content)

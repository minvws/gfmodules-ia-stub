import configparser
import json
import os
from typing import Any, Union

from app.config.schemas import Config
from app.config.services import ConfigParser
from app.schemas import UziAttributes

def root_path(*args: str) -> str:
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", *args),
    )

def load_config(config_file: str) -> Config:
    config_parser = ConfigParser(
        config_parser=configparser.ConfigParser(
            interpolation=configparser.ExtendedInterpolation(),
        ),
        config_path=root_path(config_file),
    )
    return config_parser.parse()

def file_content(filepath: str) -> Union[str, None]:
    if filepath is not None and os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as file:
            return file.read()
    return None

def file_content_raise_if_none(filepath: str) -> str:
    optional_file_content = file_content(filepath)
    if optional_file_content is None:
        raise ValueError(f"file_content for {filepath} shouldn't be None")
    return optional_file_content

def json_from_file(filepath: str) -> Any:
    return json.loads(file_content_raise_if_none(filepath))

def mocked_bsn_to_uzi_data(
    bsn: str,
    filepath: str,
) -> UziAttributes:
    uzi_data = json_from_file(filepath)
    instance = UziAttributes(**uzi_data[bsn])
    return instance
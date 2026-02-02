import configparser
import os
from typing import Any
from app.config.schemas import Config
from app.config.services import ConfigParser
from max_core.misc.utils import json_from_file


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

def mocked_bsn_to_dezi_data(
    bsn: str,
    filepath: str,
) -> Any:
    return json_from_file(filepath)[bsn]
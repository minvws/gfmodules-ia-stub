import logging

import json
from pathlib import Path
from fastapi import APIRouter, Depends, Response
import inject

from app.config.schemas import Config

logger = logging.getLogger(__name__)
router = APIRouter()

# https://www.patorjk.com/software/taag/#p=display&f=Doom&t=Skeleton
LOGO = r"""
 _____  ___             _         _     
|_   _|/ _ \           | |       | |    
  | | / /_\ \______ ___| |_ _   _| |__  
  | | |  _  |______/ __| __| | | | '_ \ 
 _| |_| | | |      \__ \ |_| |_| | |_) |
 \___/\_| |_/      |___/\__|\__,_|_.__/ 
"""


@router.get("/")
def index(
    config: Config = Depends(lambda: inject.instance(Config)),
) -> Response:
    content = LOGO

    try:
        with open(Path(__file__).parent.parent.parent / config.app.version_file_path, "r") as file:
            data = json.load(file)
            content += "\nVersion: %s\nCommit: %s" % (data["version"], data["git_ref"])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        content += "\nNo version information found"
        logger.info("Version info could not be loaded: %s" % e)

    return Response(content)


@router.get("/version.json")
def version_json(
    config: Config = Depends(lambda: inject.instance(Config)),
) -> Response:
    try:
        with open(Path(__file__).parent.parent.parent / config.app.version_file_path, "r") as file:
            content = file.read()
    except FileNotFoundError as e:
        logger.info("Version info could not be loaded: %s" % e)
        return Response(status_code=404)

    return Response(content)

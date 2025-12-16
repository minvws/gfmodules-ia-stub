import json
import logging
from typing import Any, Dict

import inject
import uvicorn
from fastapi import FastAPI

from max_core.application import setup_max_core

from app.bindings import AppBindings
from app.config.schemas import Config, UvicornConfig
from app.docs import init_docs_module
from app.utils import load_config
from app.routers.default import router as default_router
from app.routers.health import router as health_router


def kwargs_from_config(config: UvicornConfig) -> Dict[str, Any]:
    kwargs = {
        "host": config.host,
        "port": config.port,
        "reload": config.reload,
        "proxy_headers": True,
        "workers": config.workers,
    }

    if config.reload_includes is not None and config.reload_includes != "":
        kwargs["reload_includes"] = config.reload_includes.split(" ")

    if config.use_ssl:
        if config.base_dir is None:
            raise ValueError("base_dir must not be None when use_ssl is True")
        if config.key_file is None:
            raise ValueError("key_file must not be None when use_ssl is True")
        if config.cert_file is None:
            raise ValueError("cert_file must not be None when use_ssl is True")

        kwargs["ssl_keyfile"] = config.base_dir + "/" + config.key_file
        kwargs["ssl_certfile"] = config.base_dir + "/" + config.cert_file

    return kwargs


def run() -> None:
    config = _load_config_once()
    uvicorn.run(
        "app.application:uvicorn_app_factory",
        factory=True,
        **kwargs_from_config(config.uvicorn)
    )


def uvicorn_app_factory() -> FastAPI:
    config = _load_config_once()
    return create_app(config)


def create_app(config: Config) -> FastAPI:
    version = _load_version(config.app.version_file_path)
    logging.basicConfig(level=config.app.loglevel.upper())

    inject.configure_once(
        AppBindings(config),
        allow_override=True,
    )

    app = FastAPI(
        title="IA-stub",
        summary="Identification Authorization Stub for GFModules",
        version=version,
        docs_url=None,
        redoc_url=None,
        openapi_url=config.swagger.openapi_endpoint if config.swagger.enabled else None,
    )

    setup_max_core(app, config)
    init_docs_module(app)
    app.include_router(default_router)
    app.include_router(health_router)

    return app


def _load_config_once() -> Config:
    return load_config("app.conf")


def _load_version(file_path: str) -> str:
    with open(file_path, encoding="utf-8") as file:
        version_data: Dict[str, Any] = json.load(file)
    version = version_data.get("version", "v0.0.0")
    if not isinstance(version, str):
        raise ValueError("Version file is missing 'version' field or it is not a string")
    return version
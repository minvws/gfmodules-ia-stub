from pydantic import BaseModel, Field

from max_core.config.schemas import CoreConfig
from max_core.config.schemas import AppConfig as CoreAppConfig


class AppConfig(CoreAppConfig):
    version_file_path: str = Field(default="static/version.json")
    mocked_dezi_data_file_path: str = Field(default="dezi_data.json")
    mocked_identities_file_path: str = Field(default="digid_mock_identities.json")

class UvicornConfig(BaseModel):
    host: str
    port: int
    reload: bool = Field(default=False)
    workers: int = Field(default=1)
    use_ssl: bool = Field(default=False)
    base_dir: str | None = Field(default=None)
    cert_file: str | None = Field(default=None)
    key_file: str | None = Field(default=None)
    reload_includes: str | None = Field(default=None)


class SwaggerConfig(BaseModel):
    enabled: bool = Field(default=False)
    swagger_ui_endpoint: str | None = Field(default="/docs")
    redoc_endpoint: str | None = Field(default="/redocs")
    openapi_endpoint: str | None = Field(default="/openapi.json")


class Config(CoreConfig):
    app: AppConfig
    uvicorn: UvicornConfig
    swagger: SwaggerConfig = Field(default_factory=SwaggerConfig)

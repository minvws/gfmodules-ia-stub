from pydantic import Field

from max_core.config.schemas import CoreConfig
from max_core.config.schemas import AppConfig as CoreAppConfig


class AppConfig(CoreAppConfig):
    custom_config: int = Field(default=123)

class YourAppConfig(CoreConfig):
    app: AppConfig
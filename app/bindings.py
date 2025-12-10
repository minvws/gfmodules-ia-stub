from inject import Binder

from app.config import YourAppConfig
from max_core.bindings import MaxCoreBindings
from max_core.bindings.userinfo_bindings import UserinfoBindings

class AppBindings:
    def __init__(self, config: YourAppConfig) -> None:
        self.__config = config

    def __call__(self, binder: Binder) -> None:
        binder.install(MaxCoreBindings(self.__config))

        # Replace the example UserinfoService with your custom implementation
        UserinfoBindings.bind_bsn_userinfo_service(self.__config, binder)
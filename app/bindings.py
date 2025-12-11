from logging import Logger, getLogger

from inject import Binder

from max_core.bindings import MaxCoreBindings

from app.config.schemas import Config
from app.docs.bindings import DocsBindings
from max_core.providers.digid_mock_provider import DigidMockProvider as maxDigidMockProvider
from app.providers.digid_mock_provider import DigidMockProvider
from app.userinfo.bindings import UserinfoBindings
from app.utils import json_from_file

class AppBindings:
    def __init__(self, config: Config) -> None:
        self.__config = config

    def __call__(self, binder: Binder) -> None:
        binder.install(MaxCoreBindings(self.__config))

        binder.bind(Logger, getLogger())
        binder.install(DocsBindings(self.__config.swagger))
        
        identities = json_from_file(self.__config.app.mocked_identities_file_path)
        binder.bind_to_constructor(maxDigidMockProvider, lambda: DigidMockProvider(identities))
        
        UserinfoBindings.bind_bsn_userinfo_service(self.__config, binder)
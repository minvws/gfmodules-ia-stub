from inject import Binder
import inject
from max_core.services.userinfo.userinfo_service import UserinfoService
from app.config.schemas import Config

from app.services.encryption.declaration_jwt_service import DeclarationJWTService
from app.services.encryption.envelope_jwt_service import EnvelopeJWTService
from app.userinfo.services import IAUserinfoService, UserinfoProvider

class UserinfoBindings:
    @staticmethod
    def bind_bsn_userinfo_service(config: Config,  binder: Binder) -> None:

        binder.bind_to_constructor(
            UserinfoProvider,
            lambda: UserinfoProvider(config.app.mocked_dezi_data_file_path)
        )

        binder.bind_to_constructor(
            UserinfoService,
            lambda: IAUserinfoService(
                userinfo_provider=inject.instance(UserinfoProvider),
                declaration_jwt_service=inject.instance(DeclarationJWTService),
                envelope_jwt_service=inject.instance(EnvelopeJWTService),
            ),
        )

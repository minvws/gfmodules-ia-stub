from inject import Binder
import inject
from max_core.services.userinfo.userinfo_service import UserinfoService
from app.config.schemas import Config

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
                req_issuer=config.oidc.issuer,
                jwt_expiration_duration=config.oidc.jwt_expiration_duration,
                jwt_nbf_lag=config.oidc.jwt_nbf_lag,
                userinfo_provider=inject.instance(UserinfoProvider),
            ),
        )

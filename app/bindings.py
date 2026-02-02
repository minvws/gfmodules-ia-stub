from logging import Logger, getLogger

from inject import Binder

from max_core.bindings import MaxCoreBindings

from app.config.schemas import Config
from app.docs.bindings import DocsBindings
from max_core.providers.digid_mock_provider import DigidMockProvider as maxDigidMockProvider
from app.providers.digid_mock_provider import DigidMockProvider
from app.services.encryption.declaration_jwt_service import DeclarationJWTService
from app.services.encryption.envelope_jwt_service import EnvelopeJWTService
from app.userinfo.bindings import UserinfoBindings
from max_core.misc.utils import load_certificate_with_jwk_from_path, load_jwk, json_from_file

class AppBindings:
    def __init__(self, config: Config) -> None:
        self.__config = config

    def __call__(self, binder: Binder) -> None:
        binder.bind_to_constructor(
            EnvelopeJWTService,
            lambda: EnvelopeJWTService(
                issuer=self.__config.oidc.issuer,
                signing_private_key=load_jwk(self.__config.jwe.jwe_sign_priv_key_path),
                signing_certificate=load_certificate_with_jwk_from_path(
                    self.__config.jwe.jwe_sign_crt_path
                ),
                exp_margin=self.__config.oidc.jwt_expiration_duration,
                json_schema="https://example.com",
                loa_authn="http://eidas.europa.eu/LoA/high",
            ),
        )
        base_url = self.__config.app.external_base_url or "https://localhost:8006"
        binder.bind_to_constructor(
            DeclarationJWTService,
            lambda: DeclarationJWTService(
                issuer=self.__config.oidc.issuer,
                signing_private_key=load_jwk(self.__config.oidc.rsa_private_key),
                signing_certificate=load_certificate_with_jwk_from_path(
                    self.__config.oidc.rsa_private_key_crt
                ),
                exp_margin=self.__config.oidc.jwt_expiration_duration,
                json_schema="https://example.com",
                jku=base_url + self.__config.oidc.jwks_endpoint,
            ),
        )
        binder.install(MaxCoreBindings(self.__config))

        binder.bind(Config, self.__config)
        binder.bind(Logger, getLogger())
        binder.install(DocsBindings(self.__config.swagger))
        
        identities = json_from_file(self.__config.app.mocked_identities_file_path)
        binder.bind_to_constructor(maxDigidMockProvider, lambda: DigidMockProvider(identities))

        UserinfoBindings.bind_bsn_userinfo_service(self.__config, binder)
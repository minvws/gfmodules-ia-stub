import time
from uuid import uuid4

from inject import autoparams
from max_core.models.auth_session import AuthSession
from max_core.models.authentication_context import AuthenticationContext
from max_core.models.saml.artifact_response import ArtifactResponse
from max_core.models.userinfo import Userinfo
from max_core.services.auth_session.auth_session_encrypter import AuthSessionEncrypter
from max_core.services.userinfo.userinfo_service import UserinfoService
from max_core.storage.auth_session_cache import AuthSessionCache
from max_core.services.client_repository import ClientRepository

from app.schemas import DeziAttributes
from app.services.encryption.rsa_jwe_service import RSAJweService
from app.utils import mocked_bsn_to_dezi_data


class UserinfoProvider:
    @autoparams("auth_session_cache", "auth_session_encrypter")
    def __init__(
        self,
        mocked_dezi_data_file_path: str,
        auth_session_cache: AuthSessionCache,
        auth_session_encrypter: AuthSessionEncrypter,
    ) -> None:
        self._mocked_dezi_data_file_path = mocked_dezi_data_file_path

    def exchange_bsn(self, bsn: str) -> DeziAttributes:

        dezi_data = mocked_bsn_to_dezi_data(bsn, self._mocked_dezi_data_file_path)

        return DeziAttributes(
            **dezi_data.model_dump(),
        )


class IAUserinfoService(UserinfoService):
    CONTENT_TYPE = "application/jwt"

    @autoparams("jwe_service", "client_repository")
    def __init__(
        self,
        req_issuer: str,
        jwt_expiration_duration: int,
        jwt_nbf_lag: int,
        jwe_service: RSAJweService,
        client_repository: ClientRepository,
        userinfo_provider: UserinfoProvider,
    ):
        self._jwe_service = jwe_service
        self._client_repository = client_repository
        self._req_issuer = req_issuer
        self._jwt_expiration_duration = jwt_expiration_duration
        self._jwt_nbf_lag = jwt_nbf_lag
        self._userinfo_provider = userinfo_provider

    def request_userinfo_for_saml_artifact(
        self,
        authentication_context: AuthenticationContext,
        artifact_response: ArtifactResponse,
        subject_identifier: str,
    ) -> Userinfo:
        client_id = authentication_context.authorization_request["client_id"]
        client = self._client_repository.get_by_id(client_id)
        pubkey_content = client.get_public_key_jwk().export_to_pem().decode("utf-8")

        bsn = artifact_response.get_bsn(authorization_by_proxy=False)
        
        userinfo = self._userinfo_provider.exchange_bsn(bsn)

        jwe = self._jwe_service.to_jwe(
            {
                **userinfo.model_dump(),
                "jti": str(uuid4()),
                "iat": int(time.time()) - self._jwt_nbf_lag,
                "exp": int(time.time()) + self._jwt_expiration_duration,
                "iss": self._req_issuer,
                "sub": subject_identifier,
                "aud": client_id,
                "loa_authn": "http://eidas.europa.eu/LoA/high",
                "json_schema": "https://example.com",
            },
            pubkey_content,
        )

        return Userinfo(body=jwe, content_type=self.CONTENT_TYPE, auth_session_id=None)

    def request_userinfo_for_session(self, auth_session: AuthSession) -> Userinfo:
        raise NotImplementedError

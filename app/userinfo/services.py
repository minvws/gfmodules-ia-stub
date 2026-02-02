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

from app.schemas import DeclarationPayloadStatic
from app.services.encryption.declaration_jwt_service import DeclarationJWTService
from app.services.encryption.envelope_jwt_service import EnvelopeJWTService
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

    def exchange_bsn(self, bsn: str) -> DeclarationPayloadStatic:
        data = mocked_bsn_to_dezi_data(bsn, self._mocked_dezi_data_file_path)
        return DeclarationPayloadStatic(**data, verklaring_id=str(uuid4()))



class IAUserinfoService(UserinfoService):
    CONTENT_TYPE = "application/jwt"

    @autoparams("client_repository")
    def __init__(
        self,
        client_repository: ClientRepository,
        userinfo_provider: UserinfoProvider,
        declaration_jwt_service: DeclarationJWTService,
        envelope_jwt_service: EnvelopeJWTService,
    ):
        self._declaration_jwt_service = declaration_jwt_service
        self._envelope_jwt_service = envelope_jwt_service
        self._client_repository = client_repository
        self._userinfo_provider = userinfo_provider

    def request_userinfo_for_saml_artifact(
        self,
        authentication_context: AuthenticationContext,
        artifact_response: ArtifactResponse,
        subject_identifier: str,
    ) -> Userinfo:
        client_id = authentication_context.authorization_request["client_id"]
        client = self._client_repository.get_by_id(client_id)
        pubkey_content = client.certificate

        bsn = artifact_response.get_bsn(authorization_by_proxy=False)
        
        dezi_payload_static = self._userinfo_provider.exchange_bsn(bsn)
        declaration_jwt = self._declaration_jwt_service.create_jwt(dezi_payload_static)
        jwe = self._envelope_jwt_service.create_jwe(
            aud=client_id,
            declaration=declaration_jwt,
            encryption_certificate=pubkey_content,
            declaration_id=dezi_payload_static.verklaring_id,
            sub=subject_identifier,
        )

        return Userinfo(body=jwe, content_type=self.CONTENT_TYPE, auth_session_id=None)

    def request_userinfo_for_session(self, auth_session: AuthSession) -> Userinfo:
        raise NotImplementedError

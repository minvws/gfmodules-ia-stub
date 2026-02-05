import logging
import time
from uuid import uuid4

from jwcrypto.jwk import JWK
from jwcrypto.jwt import JWT

from max_core.models.certificate_with_jwk import CertificateWithJWK

from app.schemas import DeclarationHeader, DeclarationPayloadDynamic, DeclarationPayloadStatic

logger = logging.getLogger(__name__)


class DeclarationJWTService:
    def __init__(
        self,
        issuer: str,
        signing_private_key: JWK,
        signing_certificate: CertificateWithJWK,
        jku: str,
        exp_margin: int,
        json_schema: str,
    ) -> None:
        self.__signing_private_key = signing_private_key
        self._signing_certificate = signing_certificate
        self.issuer = issuer
        self.jku = jku
        self.exp_margin = exp_margin
        self.json_schema = json_schema

    def create_jwt(self, static_payload: DeclarationPayloadStatic) -> str:
        logger.debug("Creating declaration JWT for verklaring_id=%s", static_payload.verklaring_id)
        jwt_header = DeclarationHeader(
            alg="RS256",
            kid=self._signing_certificate.kid,
            jku=self.jku,
            typ="JWT",
        )
        now = int(time.time())
        dynamic_payload = DeclarationPayloadDynamic(
            jti=str(uuid4()),
            exp=now + self.exp_margin,
            nbf=now,
            iss=self.issuer,
            json_schema=self.json_schema,
        )

        jwt_token = JWT(
            header=jwt_header.model_dump(),
            claims={**static_payload.model_dump(), **dynamic_payload.model_dump()},
        )
        jwt_token.make_signed_token(self.__signing_private_key)
        return jwt_token.serialize()  # type: ignore

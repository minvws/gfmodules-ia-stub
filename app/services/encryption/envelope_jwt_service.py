import logging
import time
from uuid import uuid4

from jwcrypto.jwk import JWK
from jwcrypto.jwt import JWT

from max_core.models.certificate_with_jwk import CertificateWithJWK

from app.schemas import EnvelopeJWEHeader, EnvelopeJWTHeader, EnvelopeJWTPayload

JWE_ENC = "A128CBC-HS256"
JWE_ALG = "RSA-OAEP"
JWE_CTY = "JWT"
JWE_TYP = "JWT"
JWT_ALG = "RS256"

logger = logging.getLogger(__name__)


class EnvelopeJWTService:
    def __init__(
        self,
        issuer: str,
        signing_private_key: JWK,
        signing_certificate: CertificateWithJWK,
        exp_margin: int,
        json_schema: str,
        loa_authn: str,
    ) -> None:
        self.__signing_private_key = signing_private_key
        self._signing_certificate = signing_certificate
        self.issuer = issuer
        self.exp_margin = exp_margin
        self.json_schema = json_schema
        self.loa_authn = loa_authn

    def create_jwt(self, aud:str, declaration: str, declaration_id: str, sub: str) -> str:
        logger.debug("Creating envelope JWT for verklaring_id=%s", declaration_id)
        jwt_header = EnvelopeJWTHeader(
            alg=JWT_ALG,
            kid=self._signing_certificate.kid,
            typ=JWE_TYP,
            cty=JWE_CTY,
        )
        now = int(time.time())
        jwt_payload = EnvelopeJWTPayload(
            jti=str(uuid4()),
            iat=now,
            exp=now + self.exp_margin,
            iss=self.issuer,
            aud=aud,
            sub=sub,
            loa_authn=self.loa_authn,
            json_schema=self.json_schema,
            verklaring=declaration,
            verklaring_id=declaration_id,
        )
        jwt_token = JWT(
            header=jwt_header.model_dump(),
            claims=jwt_payload.model_dump(),
        )
        jwt_token.make_signed_token(self.__signing_private_key)
        return jwt_token.serialize()  # type: ignore

    def create_jwe(
        self,
        aud: str,
        encryption_certificate: CertificateWithJWK,
        declaration: str,
        declaration_id: str,
        sub: str,
    ) -> str:
        jwt_token = self.create_jwt(
            aud=aud,
            declaration=declaration,
            declaration_id=declaration_id,
            sub=sub,
        )
        jwe_header = EnvelopeJWEHeader(
            alg=JWE_ALG,
            enc=JWE_ENC,
            kid=encryption_certificate.kid,
            typ=JWE_TYP,
            cty=JWE_CTY,
        )
        jwe_token = JWT(header=jwe_header.model_dump(), claims=jwt_token)
        jwe_token.make_encrypted_token(encryption_certificate.jwk)
        return jwe_token.serialize()  # type: ignore

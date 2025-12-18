import configparser
import json
import os
from typing import Any, Dict, Tuple, Union
from uuid import uuid4
from time import time
import inject
from jwcrypto import jwt, jwk
from app.config.schemas import Config
from app.config.services import ConfigParser
from app.schemas import DeclarationHeader, DeclarationPayload, DeziAttributes
from max_core.misc.utils import kid_from_certificate

def root_path(*args: str) -> str:
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", *args),
    )

def load_config(config_file: str) -> Config:
    config_parser = ConfigParser(
        config_parser=configparser.ConfigParser(
            interpolation=configparser.ExtendedInterpolation(),
        ),
        config_path=root_path(config_file),
    )
    return config_parser.parse()

def file_content(filepath: str) -> Union[str, None]:
    if filepath is not None and os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as file:
            return file.read()
    return None

def file_content_raise_if_none(filepath: str) -> str:
    optional_file_content = file_content(filepath)
    if optional_file_content is None:
        raise ValueError(f"file_content for {filepath} shouldn't be None")
    return optional_file_content

def json_from_file(filepath: str) -> Any:
    return json.loads(file_content_raise_if_none(filepath))

def mocked_bsn_to_dezi_data(
    bsn: str,
    filepath: str,
) -> DeziAttributes:
    declaration_data = json_from_file(filepath)
    jwt_str, verklaring_id = create_declaration_jwt(declaration_data[bsn])

    return DeziAttributes(
        verklaring_id=verklaring_id,
        verklaring=jwt_str,
    )

def create_declaration_jwt(declaration: Dict[str, Any]) -> Tuple[str, str]:
    config = inject.instance(Config)
    if not config.app.external_base_url:
        raise ValueError("external_base_url must be set in config to create declaration JWT")
    jku = config.app.external_base_url + config.oidc.jwks_endpoint

    signing_cert = file_content_raise_if_none(
        config.app.mocked_declaration_signing_cert_path
    )
    kid = kid_from_certificate(signing_cert)

    header = DeclarationHeader(
        alg="RS256",
        kid=kid,
        jku=jku,
        typ="JWT",
    )
    verklaring_id=str(uuid4())
    claims = DeclarationPayload(
        jti=str(uuid4()),
        iss="abonnee.dezi.nl",
        exp=int(time()) + 3600,
        nbf=int(time()),
        json_schema="https://example.com",
        verklaring_id=verklaring_id,
        **declaration
    )
    # Load RSA private key (PEM)
    private_key_pem = file_content_raise_if_none(
        config.app.mocked_declaration_signing_key_path
    )
    key = jwk.JWK.from_pem(private_key_pem.encode())

    token = jwt.JWT(
        header=header.model_dump(),
        claims=claims.model_dump(),
    )
    token.make_signed_token(key)

    return token.serialize(), verklaring_id
    
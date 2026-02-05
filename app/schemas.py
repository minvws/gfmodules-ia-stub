from pydantic import BaseModel

class DeclarationPayloadDynamic(BaseModel):
    jti: str
    iss: str
    exp: int
    nbf: int
    json_schema: str

class DeclarationPayloadStatic(BaseModel):
    loa_dezi: str
    verklaring_id: str
    dezi_nummer: str
    voorletters: str
    voorvoegsel: str
    achternaam: str
    abonnee_nummer: str
    abonnee_naam: str
    rol_code: str
    rol_naam: str
    rol_code_bron: str
    status_uri: str

class DeclarationHeader(BaseModel):
    alg: str
    kid: str
    jku: str
    typ: str

class EnvelopeJWEHeader(BaseModel):
    alg: str
    enc: str
    kid: str
    typ: str
    cty: str

class EnvelopeJWTHeader(BaseModel):
    alg: str
    kid: str
    typ: str
    cty: str

class EnvelopeJWTPayload(BaseModel):
    jti: str
    iat: int
    exp: int
    iss: str
    aud: str
    sub: str
    loa_authn: str
    json_schema: str
    verklaring: str
    verklaring_id: str
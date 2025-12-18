from pydantic import BaseModel

class DeclarationPayload(BaseModel):
    jti: str
    iss: str
    exp: int
    nbf: int
    json_schema: str
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
    revocatie_controle_uri: str

class DeclarationHeader(BaseModel):
    alg: str
    kid: str
    jku: str
    typ: str

class DeziAttributes(BaseModel):
    verklaring_id: str
    verklaring: str


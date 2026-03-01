from pydantic import BaseModel


class JWK(BaseModel):
    kty: str = "EC"
    crv: str = "P-256"
    x: str
    y: str
    use: str = "sig"
    kid: str = "1"

class JWKS(BaseModel):
    keys: list[JWK]

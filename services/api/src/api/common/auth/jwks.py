import base64

from api.models.JWKS import JWK, JWKS
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
)
from jwt import PyJWK

_private_key = ec.generate_private_key(ec.SECP256R1())
_private_bytes = _private_key.private_bytes(
    encoding=Encoding.PEM,
    format=PrivateFormat.PKCS8,
    encryption_algorithm=NoEncryption(),
)


def _bincode(n: int):
    return (
        base64.urlsafe_b64encode(n.to_bytes(32, byteorder="big"))
        .decode("ascii")
        .rstrip("=")
    )


_numbers = _private_key.public_key().public_numbers()
_key = JWK(
    x=_bincode(_numbers.x),
    y=_bincode(_numbers.y),
)
_pyjwk = PyJWK(_key.model_dump())
_jwks = JWKS(keys=[_key])


def get_jwks():
    return _jwks


def get_public_key():
    return _pyjwk


def get_private_key():
    return _private_bytes


__all__ = ["get_jwks", "get_public_key", "get_private_key"]

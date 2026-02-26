from auth.models.Token import Token


class RefreshToken(Token):
    type: str = "refresh"

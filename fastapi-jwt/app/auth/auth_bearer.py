from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .auth_handler import decode_token


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request=request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid scheme")
            if not self.verify_token(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid Token or token expired")
            return credentials.credentials
        else:
            return HTTPException(status_code=403, detail="Invalid Authorization code")

    def verify_token(self, token: str) -> bool:
        verified = False
        try:
            payload = decode_token(token)
        except:
            payload = None
        if payload:
            verified = True
            return verified
        else:
            return verified

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.jwt_handler import decode_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme.lower() == "bearer":
                raise HTTPException(
                    status_code=403,
                    detail="Invalid authentication scheme. Use 'Bearer'."
                )
            return credentials.credentials
        else: 
            raise HTTPException(
                    status_code=403,
                    detail="Invalid authentication scheme. Use 'Bearer'."
                )

    def verify_jwt(self, token: str) -> bool:
        isTokenValid = False
        payload = decode_jwt(token)
        if payload:
            isTokenValid = True
        return isTokenValid

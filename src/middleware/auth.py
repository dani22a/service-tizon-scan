"""
Middleware de autenticación JWT que protege todas las rutas excepto las públicas.
Lee el token del header Authorization: Bearer <token> o del body como fallback.
"""
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi import HTTPException
from src.lib.jwt import verify_token, get_user_id
import json
import logging

logger = logging.getLogger("LOGGER_AUTH")

PUBLIC_ROUTES = [
    "/api/v1/login",
    "/api/v1/register",
    "/docs",
    "/public",
    "/train",
]


class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Permitir peticiones OPTIONS (preflight de CORS) sin autenticación
        if request.method == "OPTIONS":
            return await call_next(request)
        
        # Permitir rutas públicas sin autenticación
        if any(request.url.path.startswith(route) for route in PUBLIC_ROUTES):
            return await call_next(request)

        token = self._extract_token(request)

        if not token:
            logger.warning("401 no token | method=%s path=%s", request.method, request.url.path)
            return JSONResponse(
                status_code=401,
                content={
                    "status": "error",
                    "message": "No token provided",
                    "data": None,
                },
            )

        try:
            payload = verify_token(token)
            user_id = payload["user_id"]

            request.state.user_id = user_id
            request.state.user_email = payload.get("email")

        except HTTPException as e:
            logger.warning("401 invalid token | method=%s path=%s detail=%s", request.method, request.url.path, e.detail)
            return JSONResponse(
                status_code=e.status_code,
                content={
                    "status": "error",
                    "message": e.detail,
                    "data": None,
                },
            )
        except Exception as e:
            logger.warning("401 token exception | method=%s path=%s detail=%s", request.method, request.url.path, str(e))
            return JSONResponse(
                status_code=401,
                content={
                    "status": "error",
                    "message": f"Invalid token: {str(e)}",
                    "data": None,
                },
            )

        response = await call_next(request)
        return response

    def _extract_token(self, request: Request) -> str | None:
        auth_header = request.headers.get("Authorization")
                
        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == "bearer":
                return parts[1]

        return None

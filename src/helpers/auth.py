from fastapi import Request, HTTPException

def get_current_user_id(request: Request) -> int:
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")
    return user_id


def get_current_user_email(request: Request) -> str:
    email = getattr(request.state, "user_email", None)
    if not email:
        raise HTTPException(status_code=401, detail="User not authenticated")
    return email


def extract_token_from_request(request: Request) -> str | None:
    auth_header = request.headers.get("Authorization")
    if auth_header:
        parts = auth_header.split()
        if len(parts) == 2 and parts[0].lower() == "bearer":
            return parts[1]
    
    token_param = request.query_params.get("token")
    if token_param:
        return token_param
    
    return None

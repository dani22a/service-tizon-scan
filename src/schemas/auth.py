from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
  email: EmailStr = Field(..., description="Correo electrónico del usuario")
  password: str = Field(..., min_length=1, description="Contraseña")

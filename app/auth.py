from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # HER TOKENI KABUL ET! 🚀
    return {"id": 1, "email": "test@example.com", "role": "AGENT"}

def get_password_hash(password):
    return password  # Şifreleme yapma!

def verify_password(plain_password, hashed_password):
    return plain_password == hashed_password  # Basit kontrol

def create_access_token(data: dict):
    return "test-token-123"  # Sabit token döndür
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from app.core.settings import security_settings as S

pwd_ctx = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__time_cost=S.argon2_time_cost,
    argon2__memory_cost=S.argon2_memory_cost,
    argon2__parallelism=S.argon2_parallelism,
)

def get_password_hash(p: str)->str:
    return pwd_ctx.hash(p)

def verify_password(p: str, h: str)->bool:
    return pwd_ctx.verify(p, h)

def create_access_token(subject: str, expires_delta: timedelta|None=None):
    now=datetime.now(timezone.utc)
    exp=now+(expires_delta or timedelta(minutes=S.access_token_exp_minutes))
    payload={"sub":subject,"iat":int(now.timestamp()),"exp":int(exp.timestamp())}
    key=S.secret_key.get_secret_value() if S.secret_key else "devkey"
    return jwt.encode(payload, key, algorithm=S.jwt_algorithm)

def verify_access_token(token:str):
    key=S.secret_key.get_secret_value() if S.secret_key else "devkey"
    return jwt.decode(token, key, algorithms=[S.jwt_algorithm])

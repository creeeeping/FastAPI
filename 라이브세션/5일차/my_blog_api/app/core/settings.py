from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class SecuritySettings(BaseSettings):
    jwt_algorithm: str = "HS256"
    access_token_exp_minutes: int = 60
    secret_key: SecretStr|None=None
    argon2_time_cost:int=3
    argon2_memory_cost:int=32768
    argon2_parallelism:int=1
    model_config=SettingsConfigDict(env_file=".env", extra="ignore")

security_settings = SecuritySettings()

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    HUBSPOT_CLIENT_ID:str
    HUBSPOT_CLIENT_SECRET:str
    HUBSPOT_REDIRECT_URI:str
    GROQ_API_KEY:str
    MODEL_NAME:str
    HUBSPOT_BASE_URL:str
    API_BASE_URL:str

    EMAIL_SMTP_SERVER: str = "smtp.gmail.com"
    EMAIL_SMTP_PORT: int = 587
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str

    API_TIMEOUT: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
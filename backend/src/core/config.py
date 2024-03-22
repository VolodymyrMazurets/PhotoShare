# CONFIG WILL BE THERE
from pydantic_settings import BaseSettings

class Settings(BaseSettings):  
    sqlalchemy_database_url: str 
    secret_key: str 
    algorithm: str 
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    cloudinary_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str
    

    class Config:
        extra = 'allow'
        env_file = ".env"
        env_file_encoding = "utf-8"
        
settings = Settings()

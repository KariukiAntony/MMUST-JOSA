import os
from decouple import config
from datetime import timedelta
class Config:
     SECRET_KEY = config("SECRET_KEY")

class DevConfig(Config):
     SQLALCHEMY_DATABASE_URI = config("DATABASE_URI")
     SQLALCHEMY_TIMEZONE = 'Africa/Nairobi'
     SQLALCHEMY_TRACK_MODIFICATION = False
     DEBUG = True
     JWT_SECRET_KEY = config("JWT_SECRET_KEY") 
     JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
     JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)
     CORS_HEADERS = "Content-Type"


class TestConfig(DevConfig):
     SQLALCHEMY_TRACK_MODIFICATION = True
     TESTING = True

class ProdConfig(Config):
     pass


config_dict = {
     
     "dev": DevConfig,
     "test": TestConfig,
     "prod": ProdConfig
}
     


class Config:
     SECRET_KEY = "secret_key"

class DevConfig(Config):
     SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
     SQLALCHEMY_TRACK_MODIFICATION = False
     DEBUG = False

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
     
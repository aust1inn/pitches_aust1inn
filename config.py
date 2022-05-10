import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:Access@localhost/pitches'
    SECRET_KEY = os.environ.get('SECRET_KEY')


class ProdConfig(Config):
    uri = os.getenv('DATABASE_URL')
    if uri and uri.startswith('postgres://'):
        uri = uri.replace('postgres://', 'postgresql://', 1)
        
    SQLALCHEMY_DATABASE_URI=uri    


class DevConfig(Config):
    # DEBUG = True
    pass

config_options = {
'development':DevConfig,
'production':ProdConfig
}
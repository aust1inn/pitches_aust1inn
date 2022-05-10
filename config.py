import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')


class ProdConfig(Config):
    # uri = os.getenv('DATABASE_URL')
    # if uri and uri.startswith('postgres://'):
    #     uri = uri.replace('postgres://', 'postgresql://', 1)
        
    # SQLALCHEMY_DATABASE_URI=uri  
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL').replace ('://', 'ql://', 1)  


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:Access@localhost/pitches'

config_options = {
'development':DevConfig,
'production':ProdConfig
}
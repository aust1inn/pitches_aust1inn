from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config_options
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

bootstrap = Bootstrap()
db = SQLAlchemy()
bcrypt =Bcrypt()
login_manager=LoginManager()
login_manager.login_view ='login'
login_manager.login_message_category='info'

def create_app(config_name):

    app = Flask(__name__)

    # Creating the app configurations
    app.config.from_object(config_options[config_name])

    # Initializing flask extensions
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Will add the views and forms
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
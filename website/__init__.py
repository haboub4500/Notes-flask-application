#whenver we put __init__.py file in a folder : that flder becomes a python package which we can import

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import sqlite3
import _sqlite3
from flask_login import LoginManager, login_manager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app() :
    app = Flask(__name__) # name = nameof the file (main)
    #app.config['SECRET KEY'] = 'this is the encryption key' # encrypt and secure cookies and scripts related to our session data related to the website 
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    from .models import User, Note
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

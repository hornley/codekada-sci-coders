from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy object
db = SQLAlchemy()

# App factory to initialize Flask with SQLAlchemy
def init_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

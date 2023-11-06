from flask import Flask, jsonify
from src.config.config import config_dict
from src.models.database import db, migrate, User
from os import path
from src.auth.auth import auth
from src.views.blogs import blogs
from flask_jwt_extended import JWTManager

""" A function for creating an application """
def create_app(config = config_dict["dev"]):
     
     app = Flask(__name__)
     app.config.from_object(config)
     db.init_app(app=app)
     migrate.init_app(app=app)
     JWTManager(app)

     create_database(app=app)

     @app.errorhandler(404)
     def handle_not_found(e):
         return jsonify({"error": str(e)})
     

     @app.errorhandler(500)
     def handle_Internal_server_error(e):
         return jsonify({"error": str(e)})
     
     app.register_blueprint(auth)
     app.register_blueprint(blogs)
     
     @app.route("/")
     def index():
         return jsonify({"Hello there":" Welcome to best blogging web app" })
     
     return app


def create_database(app):
    if not path.exists("src/database.db"):
        with app.app_context():
            db.create_all()
            print("database created")
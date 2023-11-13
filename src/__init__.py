from flask import Flask, jsonify, request
from src.config.config import config_dict
from src.models.database import db, migrate, User
from src.auth.auth import auth
from src.views.blogs import blogs
from flask_jwt_extended import JWTManager
from flask_cors import CORS

""" A function for creating an application """
def create_app(config = config_dict["dev"]):
     
     app = Flask(__name__)
     app.config.from_object(config)
     db.init_app(app=app)
     migrate.init_app(app=app)
     JWTManager(app)
    #  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    #  CORS(app, resources={r"/*": {"origins": "*",
    #                              "methods": ["GET", "POST", "PATCH", "DELETE"],
    #  
     def create_database():
         with app.app_context():
            db.create_all()
            print("database tables created")
            
     required_headers = ["Content-Type", "Authorization"]
     cors = CORS(app, resources={r"/*": {
      "origins": "*",
      "methods": ["GET", "POST", "PATCH", "DELETE"],
      "supports_credentials": True,
      "allow_headers": required_headers
     }})

     create_database()


    #  @app.before_request
    #  def before_request():
    #     if "Origin" in request.headers:
    #         request.headers.add('Access-Control-Allow-Origin', '*')
    #         request.headers.add('Access-Control-Allow-Headers', ', '.join(required_headers))

     @app.after_request
     def add_security_header(response):
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = ", ".join(required_headers)
        return response
     
     @app.get("/database/danger")
     def drop_database_tables():
          with app.app_context():
            db.drop_all()
            print("all database tables droped")
            create_database()
            print("database tables created again")
            return jsonify({"success": "All database tables dropped"}) 

     @app.errorhandler(404)
     def handle_not_found(e):
         return jsonify({"error": str(e)})
     

     @app.errorhandler(500)
     def handle_Internal_server_error(e):
         return jsonify({"error": str(e)})
     
     app.register_blueprint(auth)
     app.register_blueprint(blogs)
     
     return app

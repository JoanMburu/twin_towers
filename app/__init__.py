# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_restful import Api
# from flask_jwt_extended import JWTManager
# from config import Config

# db = SQLAlchemy()
# migrate = Migrate()

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)

#     db.init_app(app)
#     migrate.init_app(app, db)
    
#     jwt = JWTManager(app)

#     from app.controllers.member_controller import MemberListResource, MemberResource
#     api = Api(app)
#     api.add_resource(MemberListResource, '/members')
#     api.add_resource(MemberResource, '/members/<int:id>')

#     return app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    
    jwt = JWTManager(app)

    from app.controllers.member_controller import MemberListResource, MemberResource
    from app.controllers.auth_controller import auth_bp  # Import the auth blueprint
    
    api = Api(app)
    api.add_resource(MemberListResource, '/members')
    api.add_resource(MemberResource, '/members/<int:id>')
    
    # Register the auth blueprint for login routes
    app.register_blueprint(auth_bp)

    return app


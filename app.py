from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from routes.member_routes import member_bp
from models import db  


migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(member_bp)

    return app

if __name__ == '__main__':
    app = create_app()  
    app.run(debug=True)

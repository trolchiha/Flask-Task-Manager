from flask import Blueprint, Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow



DB_NAME = "database.db"
db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'aecq#hbq7&afiohd@!6d*'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)
    ma.init_app(app)

    from .views import views
    from .auth import auth
    from .api import api_bp

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(api_bp)
    
    from app.models import User

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    with app.app_context():
        # db.drop_all()
        db.create_all()

    print(app.url_map)      

    return app

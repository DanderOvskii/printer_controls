from flask import Flask
from flask_login import LoginManager
from app.models import User
from dotenv import load_dotenv
import os
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY')

    # Setup flask-login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Single user instance (must match the one in auth_api)
    from app.api.auth_api import user

    @login_manager.user_loader
    def load_user(user_id):
        if str(user.id) == user_id:
            return user
        return None

    from app.api.auth_api import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    from app.api.printer_api import bp as printer_bp
    app.register_blueprint(printer_bp)

    from app.api.camera_api import bp as camera_bp
    app.register_blueprint(camera_bp)

    return app

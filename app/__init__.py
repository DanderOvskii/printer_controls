from flask import Flask


def create_app():
    app = Flask(__name__)

    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    from app.api.printer_api import bp as printer_bp
    app.register_blueprint(printer_bp)

    from app.api.camera_api import bp as camera_bp
    app.register_blueprint(camera_bp)

    return app

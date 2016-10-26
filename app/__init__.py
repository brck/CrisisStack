from flask import Flask


def create_app(config_name):
    app = Flask(__name__)

    # Register Auth blueprint to application factory
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app

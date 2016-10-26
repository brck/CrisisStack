from flask import Flask


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Register Auth blueprint to application factory
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Register Auth blueprint to application factory
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app

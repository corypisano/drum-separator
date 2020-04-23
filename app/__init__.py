
import os
from flask import Flask

from app.config import Config

def create_app(script_info=None):

    # instantiate the app
    app = Flask(
        __name__,
        template_folder="./templates",
        static_folder="./templates/static",
    )

    # set config
    app.config.from_object(Config)
    print('app config with redis: ', app.config['REDIS_URL'])

    # register blueprints
    from app.api import api

    app.register_blueprint(api)

    # shell context for flask cli
    app.shell_context_processor({"app": app})

    return app
import os
import logging

from flask import Flask

from app.config import Config

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s]: {} %(threadName)s %(levelname)s %(message)s".format(
        os.getpid()
    ),
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger()


def create_app(script_info=None):
    logger.info("create_app logger.info")
    # instantiate the app
    app = Flask(
        __name__, template_folder="./templates", static_folder="./templates/static",
    )

    # set config
    app.config.from_object(Config)

    # register blueprints
    from app.api import api

    app.register_blueprint(api)

    # shell context for flask cli
    app.shell_context_processor({"app": app})

    return app

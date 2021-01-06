import flask

from simple_vendor_matching_webhook_python import config
from simple_vendor_matching_webhook_python.webhook import vendor_matching


def create_app():
    app = flask.Flask(__name__)
    app.config.from_object(config)
    # app.config["DEBUG"] = True
    app.route("/vendor_matching", methods=["POST"])(vendor_matching)
    return app

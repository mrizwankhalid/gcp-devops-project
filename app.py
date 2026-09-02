import logging
import os
import socket

from flask import Flask, jsonify

APP_VERSION = os.environ.get("APP_VERSION", "1.0.0")
APP_ENV = os.environ.get("APP_ENV", "production")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("gcpdevops")

app = Flask(__name__)


@app.route("/")
def hello_world():
    logger.info("Handled request to /")
    return jsonify(
        message="Hello, from Flask Application",
        version=APP_VERSION,
        environment=APP_ENV,
        hostname=socket.gethostname(),
    )


@app.route("/healthz")
def healthz():
    return jsonify(status="ok"), 200


@app.route("/readyz")
def readyz():
    return jsonify(status="ready"), 200


@app.route("/info")
def info():
    return jsonify(
        version=APP_VERSION,
        environment=APP_ENV,
        hostname=socket.gethostname(),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

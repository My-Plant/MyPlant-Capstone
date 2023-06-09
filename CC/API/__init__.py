from flask import Flask, Blueprint
from dotenv import load_dotenv
import os

def create_app():
    app = Flask(__name__)

    load_dotenv()
    app.config['SECRET_KEY'] = 'akusayangkamu'
    from .auth import auth_blueprint
    from .prediction import prediction_blueprint
    from .penyakit import penyakit_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(prediction_blueprint)
    app.register_blueprint(penyakit_blueprint)

    @app.route('/', methods=['GET'])
    def default():
        return 'Response Success'
    return app
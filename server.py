import os
import auth
import sleep

from flask import (
    Flask, redirect, render_template, url_for
)
from waitress import serve


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ['SECRET_KEY'],
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

        
    app.register_blueprint(auth.bp)
    app.register_blueprint(sleep.bp)
    app.add_url_rule('/', endpoint='hello')

    return app

if __name__ == '__main__':
    PORT = os.environ.get('PORT', 8080)
    app=create_app()
    serve(app, host='0.0.0.0', port=PORT)
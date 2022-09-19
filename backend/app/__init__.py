from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from .model import db
from .database import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.app_context().push()
    db.init_app(app)
    db.create_all()
    CORS(app)
    
    from .controller import bp, restart_db
    app.register_blueprint(bp)

    @app.cli.command('db_restart')
    def db_restart():
        restart_db()
        print('Database restarted successfully!')

    # Set access control
    @app.after_request
    def after_request(res):
        res.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authentication, true')
        res.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')

        return res

    # Handle all expected errors.
    @app.errorhandler(HTTPException)
    def handle_common_errors(e):
        return jsonify({
            "success": False,
            "error": e.name,
            "message": e.description,
            "code": e.code
        }), e.code

    # Handle unknown error.
    @app.errorhandler(Exception)
    def handle_common_errors(e):
        print(e)
        return jsonify({
            "success": False,
            "error": "Unknown error",
            "message": "Something went wrong.",
            "code": 500
        }), 500

    return app

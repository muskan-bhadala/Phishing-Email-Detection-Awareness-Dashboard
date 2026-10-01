import os
from flask import Flask
from .services.database import init_db

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "dev-only-change-me"),
        DATABASE=os.path.join(app.root_path, "..", "data", "analysis_history.db"),
        MAX_CONTENT_LENGTH=int(os.getenv("MAX_CONTENT_LENGTH", 2 * 1024 * 1024)),
    )

    if test_config:
        app.config.update(test_config)

    os.makedirs(os.path.dirname(app.config["DATABASE"]), exist_ok=True)
    init_db(app.config["DATABASE"])

    from .routes import bp
    app.register_blueprint(bp)

    @app.after_request
    def security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; style-src 'self' 'unsafe-inline'; "
            "script-src 'self' 'unsafe-inline'; img-src 'self' data:;"
        )
        return response

    return app

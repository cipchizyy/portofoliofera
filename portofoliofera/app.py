import os
from flask import Flask
from dotenv import load_dotenv

from extensions import db, login_manager
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.public import public_bp
from routes.api import api_bp

load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")

# Config
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")

# Database TiDB
basedir = os.path.abspath(os.path.dirname(__file__))
ssl_ca = os.path.join(basedir, "certs", "ca-cert.pem")

ssl_str = ""
if os.path.exists(ssl_ca):
    ssl_str = f"?ssl_ca={ssl_ca}&ssl_verify_cert=true&ssl_verify_identity=true"

tidb_user = os.getenv("TIDB_USER")
tidb_password = os.getenv("TIDB_PASSWORD")
tidb_host = os.getenv("TIDB_HOST")
tidb_port = os.getenv("TIDB_PORT", "4000")
tidb_database = os.getenv("TIDB_DATABASE")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{tidb_user}:{tidb_password}"
    f"@{tidb_host}:{tidb_port}/{tidb_database}{ssl_str}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Init extensions
db.init_app(app)

login_manager.init_app(app)
login_manager.login_view = "auth.login"

# Register blueprints
app.register_blueprint(public_bp)
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(api_bp, url_prefix="/api")


@app.route("/health")
def health():
    return "OK", 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
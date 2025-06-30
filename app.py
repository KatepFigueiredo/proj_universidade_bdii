from flask import Flask
from flask_jwt_extended import JWTManager
from routes import register_blueprints
from dotenv import load_dotenv
from db import db_connection
import os
import secrets

def run():
    load_dotenv()

    app = Flask(__name__)

    jwt_secret = os.getenv("JWT_SECRET_KEY")
    if not jwt_secret:
        jwt_secret = secrets.token_urlsafe(32)
        print(f"[INFO] JWT_SECRET_KEY não definida. Chave gerada automaticamente: {jwt_secret}")

    app.config['JWT_SECRET_KEY'] = jwt_secret

    jwt = JWTManager(app)

    @app.route("/health", methods=["GET"])
    def health_check():
        return {"status": "UP"}, 200

    @app.route("/db-health", methods=["GET"])
    def db_health_check():
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("SELECT 1;")
            cur.close()
            conn.close()
            return {"database": "UP"}, 200
        except Exception as e:
            return {"database": "DOWN", "error": str(e)}, 500

    register_blueprints(app)

    app.run(debug=True)

if __name__ == "__main__":
    run()

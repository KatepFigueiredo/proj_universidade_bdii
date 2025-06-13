from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from db import db_connection
import bcrypt
from datetime import timedelta

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# REGISTO de utilizador
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    nome = data.get("nome")
    email = data.get("email")
    password = data.get("password")
    tipo = data.get("tipo_utilizador")

    if tipo not in ["estudante", "professor"]:
        return jsonify({"erro": "tipo_utilizador inválido"}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("SELECT criar_utilizador(%s, %s, %s, %s);", (nome, email, hashed_password, tipo))
        novo_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"id": novo_id, "mensagem": "Utilizador registado com sucesso"}), 201

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# LOGIN de utilizador
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    try:
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM procurar_utilizador_por_email(%s);", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if not user:
            return jsonify({"erro": "Utilizador não encontrado"}), 404

        stored_password = user[1]
        if not bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            return jsonify({"erro": "Password incorreta"}), 401
        
        expires = timedelta(hours=8)

        token = create_access_token(
            identity=str(user[0]),  # ou apenas user[0] se for int
            additional_claims={"tipo_utilizador": user[2]},
            expires_delta=expires
        )
        
        return jsonify({"token": token, "tipo": user[2]}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
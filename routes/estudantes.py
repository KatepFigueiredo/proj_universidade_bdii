from flask import Blueprint, request, jsonify
from db import db_connection

estudantes_bp = Blueprint('estudantes', __name__, url_prefix="/estudantes")

@estudantes_bp.route("/", methods=["GET"])
def listar_estudantes():
    try:
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, nome, email, data_nascimento FROM estudantes ORDER BY id")
        estudantes = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([
            {"id": e[0], "nome": e[1], "email": e[2], "data_nascimento": e[3]} for e in estudantes
        ])
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
from flask import Blueprint, request, jsonify
from decorators import role_required
from db import db_connection

professores_bp = Blueprint('professors', __name__, url_prefix="/professors")

@professores_bp.route("/", methods=["GET"])
@role_required(allowed_types=['estudante', 'professor'])
def listar_professores(conn, current_user_id):
    try:
        cur = conn.cursor()
        # Chamar a view
        cur.execute("SELECT id, nome, email, area_especializacao FROM professores_universidade;")
        professors = cur.fetchall()
        cur.close()
        return jsonify([
            {"id": p[0], "nome": p[1], "email": p[2], "area_especializacao": p[3]} for p in professors
        ])
    except Exception as e:
        return jsonify({"erro": f"Erro ao listar professores: {str(e)}"}), 500

@professores_bp.route("/<int:professor_id>/profile", methods=["PUT"])
@role_required(allowed_types=['professor'])
def atualizar_perfil_professor(professor_id, conn, current_user_id):
    
    professor_id_int = int(professor_id)
    current_user_id_int = int(current_user_id) # current_user_id vem como string do get_jwt_identity() por padrão

    if professor_id_int != current_user_id_int:
        return jsonify({"erro": "Não tem permissão para atualizar este perfil."}), 403

    data = request.json
    area_especializacao = data.get("area_especializacao")

    if not area_especializacao:
        return jsonify({"erro": "Área de especialização é obrigatória."}), 400

    try:
        cur = conn.cursor()
        # Chamar a função
        cur.execute(
            "SELECT atualizar_area_especializacao_professor(%s, %s);",
            (professor_id, area_especializacao)
        )
        conn.commit()
        cur.close()
        return jsonify({"mensagem": "Perfil do professor atualizado com sucesso."}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"erro": f"Erro ao atualizar perfil do professor: {str(e)}"}), 500
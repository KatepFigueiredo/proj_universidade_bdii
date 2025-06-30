from flask import Blueprint, request, jsonify
from decorators import role_required
from db import db_connection

participacoes_bp = Blueprint('participacoes', __name__, url_prefix="/participacoes")

@participacoes_bp.route("/matricular", methods=["POST"])
@role_required(allowed_types=['estudante'])
def matricular_estudante_na_aula(conn, current_user_id):
    data = request.json
    id_aula = data.get("id_aula")
    
    id_estudante = current_user_id

    if not id_aula:
        return jsonify({"erro": "ID da aula é obrigatório."}), 400
    
    try:
        cur = conn.cursor()
        cur.execute("CALL matricular_estudante_aula(%s, %s);", (id_estudante, id_aula))
        conn.commit()
        cur.close()
        return jsonify({"mensagem": f"Estudante {id_estudante} matriculado com sucesso na aula {id_aula}."}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"erro": f"Erro ao matricular estudante: {str(e)}"}), 500

@participacoes_bp.route("/meu-historico", methods=["GET"])
@role_required(allowed_types=['estudante', 'professor'])
def listar_minhas_aulas(conn, current_user_id):
    id_estudante_para_consultar = current_user_id

    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id_aula, data_aula, titulo_aula, hora_inicio, hora_fim, professor_nome
            FROM aulas_assistidas_por_estudante
            WHERE id_estudante = %s
            ORDER BY data_aula DESC, hora_inicio DESC;
            """,
            (id_estudante_para_consultar,)
        )
        aulas_assistidas = cur.fetchall()
        cur.close()
        
        return jsonify([
            {
                "id_aula": a[0],
                "data_aula": str(a[1]),
                "titulo_aula": a[2],
                "hora_inicio": str(a[3]),
                "hora_fim": str(a[4]),
                "professor": a[5]
            } for a in aulas_assistidas
        ])
    except Exception as e:
        return jsonify({"erro": f"Erro ao listar aulas assistidas: {str(e)}"}), 500
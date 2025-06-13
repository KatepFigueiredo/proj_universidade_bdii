from flask import Blueprint, request, jsonify
from decorators import role_required # Importe o decorador

aulas_bp = Blueprint('aulas', __name__, url_prefix="/aulas")

# Rota para listar aulas (ambos podem consultar)
@aulas_bp.route("/", methods=["GET"])
@role_required(allowed_types=['estudante', 'professor'])
def listar_aulas(conn, current_user_id):
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, titulo, data, hora_inicio, hora_fim, id_professor FROM aulas_disponiveis;")
        aulas = cur.fetchall()
        cur.close()
        return jsonify([
            {"id": a[0], "titulo": a[1], "data": str(a[2]), "hora_inicio": str(a[3]), "hora_fim": str(a[4]), "id_professor": a[5]} for a in aulas
        ])
    except Exception as e:
        return jsonify({"erro": f"Erro ao listar aulas: {str(e)}"}), 500

# Rota para criar uma nova aula (apenas professores podem)
@aulas_bp.route("/", methods=["POST"])
@role_required(allowed_types=['professor'])
def criar_aula(conn, current_user_id):
    data = request.json
    titulo = data.get("titulo")
    aula_data = data.get("data")
    hora_inicio = data.get("hora_inicio")
    hora_fim = data.get("hora_fim")
    
    id_professor = current_user_id

    if not all([titulo, aula_data, hora_inicio, hora_fim]):
        return jsonify({"erro": "Título, data, hora de início e hora de fim são obrigatórios."}), 400
    
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT criar_aula_bd(%s, %s, %s, %s, %s);",
            (titulo, aula_data, hora_inicio, hora_fim, id_professor)
        )
        novo_aula_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return jsonify({"id": novo_aula_id, "mensagem": "Aula criada com sucesso."}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"erro": f"Erro ao criar aula: {str(e)}"}), 500

# Exemplo de rota para atualizar uma aula (apenas professores)
@aulas_bp.route("/<int:aula_id>", methods=["PUT"])
@role_required(allowed_types=['professor'])
def atualizar_aula(aula_id, conn, current_user_id):
    data = request.json
    titulo = data.get("titulo")
    aula_data = data.get("data")
    hora_inicio = data.get("hora_inicio")
    hora_fim = data.get("hora_fim")

    # Opcional: Adicionar verificação para garantir que o professor só edita as suas próprias aulas
    # cur.execute("SELECT id_professor FROM aulas WHERE id = %s;", (aula_id,))
    # professor_aula = cur.fetchone()
    # if professor_aula and professor_aula[0] != current_user_id:
    #    return jsonify({"erro": "Não tem permissão para editar esta aula."}), 403

    update_fields = []
    update_values = []

    if titulo:
        update_fields.append("titulo = %s")
        update_values.append(titulo)
    if aula_data:
        update_fields.append("data = %s")
        update_values.append(aula_data)
    if hora_inicio:
        update_fields.append("hora_inicio = %s")
        update_values.append(hora_inicio)
    if hora_fim:
        update_fields.append("hora_fim = %s")
        update_values.append(hora_fim)

    if not update_fields:
        return jsonify({"erro": "Nenhum campo para atualizar fornecido."}), 400

    try:
        cur = conn.cursor()
        query = f"UPDATE aulas SET {', '.join(update_fields)} WHERE id = %s;"
        update_values.append(aula_id)
        cur.execute(query, tuple(update_values))
        conn.commit()
        cur.close()
        return jsonify({"mensagem": "Aula atualizada com sucesso."}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"erro": f"Erro ao atualizar aula: {str(e)}"}), 500
from flask import Blueprint, request, jsonify
from decorators import role_required
from db import db_connection
import base64 # Para lidar com BYTEA
from datetime import date

materiais_bp = Blueprint('materiais', __name__, url_prefix="/materiais")

@materiais_bp.route("/", methods=["POST"])
@role_required(allowed_types=['professor'])
def criar_material(conn, current_user_id):
    # --- ALTERAÇÃO AQUI: Em vez de request.json, use request.form para campos de texto ---
    titulo = request.form.get("titulo")
    tipo = request.form.get("tipo")
    autor = request.form.get("autor")
    url = request.form.get("url")
    
    # --- E aqui para o ficheiro binário, use request.files ---
    conteudo_file = request.files.get("conteudo") # Pega o objeto FileStorage do ficheiro

    if not all([titulo, tipo]):
        return jsonify({"erro": "Título e tipo de material são obrigatórios."}), 400
    
    conteudo_bytea = None
    if conteudo_file:
        try:
            # LER O CONTEÚDO BINÁRIO DO FICHEIRO
            conteudo_bytea = conteudo_file.read()
            
            # Opcional: Pode adicionar validação de tipo de ficheiro (mimetype) se for relevante
            # if conteudo_file.mimetype not in ['image/jpeg', 'image/png', 'application/pdf']:
            #     return jsonify({"erro": "Tipo de ficheiro não suportado. Apenas imagens (JPEG, PNG) e PDFs são permitidos."}), 400

        except Exception as e:
            # Capturar erros na leitura do ficheiro
            return jsonify({"erro": f"Erro ao ler o ficheiro de conteúdo: {str(e)}"}), 400

    try:
        cur = conn.cursor()
        # Chamar a função para criar material
        # O driver do PostgreSQL (psycopg2) saberá como lidar com os bytes Python para o tipo BYTEA do PostgreSQL
        cur.execute(
            "SELECT criar_material_didatico_bd(%s, %s, %s, %s, %s);",
            (titulo, tipo, autor, url, conteudo_bytea) # Passa os bytes brutos lidos do ficheiro
        )
        novo_material_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return jsonify({"id": novo_material_id, "mensagem": "Material didático criado com sucesso."}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"erro": f"Erro ao criar material didático: {str(e)}"}), 500
    
@materiais_bp.route("/recomendar", methods=["POST"])
@role_required(allowed_types=['professor'])
def recomendar_material_aula(conn, current_user_id):
    data = request.json
    id_aula = data.get("id_aula")
    id_material = data.get("id_material")
    nota = data.get("nota")
    
    id_professor = current_user_id

    # Ajuste na validação: data_aula não é mais necessária no payload
    if not all([id_aula, id_material]):
        return jsonify({"erro": "ID da aula e ID do material são obrigatórios."}), 400
    
    try:
        cur = conn.cursor()
        # Chamar a função para recomendar material (agora sem data_aula)
        cur.execute(
            "SELECT recomendar_material_aula_bd(%s, %s, %s, %s);",
            (id_aula, id_material, id_professor, nota)
        )
        novo_recomendacao_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return jsonify({"id": novo_recomendacao_id, "mensagem": "Material recomendado com sucesso na aula."}), 201
    except Exception as e:
        conn.rollback()
        if "duplicate key value violates unique constraint" in str(e):
            # A mensagem de erro agora virá do raise exception da função se a aula não existir
            return jsonify({"erro": "Este material já foi recomendado para esta aula."}), 409
        return jsonify({"erro": f"Erro ao recomendar material: {str(e)}"}), 500

@materiais_bp.route("/aula/<int:aula_id>/<string:data_aula_str>/recomendacoes", methods=["GET"])
@role_required(allowed_types=['estudante', 'professor'])
def listar_recomendacoes_por_aula(aula_id, data_aula_str, conn, current_user_id):
    try:
        data_aula = date.fromisoformat(data_aula_str)
    except ValueError:
        return jsonify({"erro": "Formato de data inválido. Use AAAA-MM-DD."}), 400

    try:
        cur = conn.cursor()
        # Chamar a view e filtrar no Flask
        cur.execute(
            """
            SELECT id, titulo_material, tipo_material, autor_material, url_material,
            nota, data_recomendacao, professor_nome
            FROM recomendacoes_detalhadas
            WHERE id_aula = %s AND data_aula = %s
            ORDER BY data_recomendacao DESC;
            """,
            (aula_id, data_aula)
        )
        recomendacoes = cur.fetchall()
        cur.close()
        
        return jsonify([
            {
                "id": r[0],
                "titulo_material": r[1],
                "tipo_material": r[2],
                "autor_material": r[3],
                "url_material": r[4],
                "nota": r[5],
                "data_recomendacao": str(r[6]),
                "professor_recomendou": r[7]
            } for r in recomendacoes
        ])
    except Exception as e:
        return jsonify({"erro": f"Erro ao listar recomendações: {str(e)}"}), 500
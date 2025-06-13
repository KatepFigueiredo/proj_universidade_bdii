# decorators.py
from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from db import db_connection

def role_required(allowed_types):  # allowed_types refere-se ao tipo_utilizador ('estudante', 'professor')
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            user_id = get_jwt_identity()
            claims = get_jwt()
            user_type = claims.get("tipo_utilizador")

            if user_type not in allowed_types:
                return jsonify({"erro": "Acesso não autorizado: tipo de utilizador sem permissão."}), 403

            # Mapeia o tipo de utilizador da aplicação para a role do PostgreSQL
            db_role = {
                "estudante": "role_estudante",
                "professor": "role_professor"
            }.get(user_type)

            if not db_role:
                return jsonify({"erro": "Erro interno: Tipo de utilizador desconhecido ou role não mapeada."}), 500

            conn = None
            try:
                conn = db_connection(role=db_role)  # A conexão é aberta com a role
                kwargs['current_user_id'] = user_id  # Passa o ID do utilizador
                kwargs['conn'] = conn  # Passa a conexão com a role aplicada
                return f(*args, **kwargs)
            except Exception as e:
                return jsonify({"erro": f"Erro na base de dados: {str(e)}"}), 500
            finally:
                if conn:
                    conn.close()  # Garante que a conexão seja fechada
        return decorated_function
    return decorator

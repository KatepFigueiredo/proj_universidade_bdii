from .estudantes import estudantes_bp
from .auth import auth_bp
from .aulas import aulas_bp
from .materiais import materiais_bp
from .professores import professores_bp
from .participacoes import participacoes_bp


def register_blueprints(app):
    app.register_blueprint(estudantes_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(aulas_bp)
    app.register_blueprint(materiais_bp)
    app.register_blueprint(professores_bp)
    app.register_blueprint(participacoes_bp)
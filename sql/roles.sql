CREATE ROLE role_estudante NOLOGIN; -- NOLOGIN: Esta role não pode ser usada para login direto
CREATE ROLE role_professor NOLOGIN; -- NOLOGIN: Esta role não pode ser usada para login direto

-- Privilégios para role_estudante (apenas consulta em todas as tabelas)
GRANT SELECT ON ALL TABLES IN SCHEMA public TO role_estudante;

-- Importante: para tabelas criadas no futuro
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public
GRANT SELECT ON TABLES TO role_estudante;

-- Privilégios para role_professor (consulta e alteração em todas as tabelas)
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO role_professor;

-- Importante: para tabelas criadas no futuro
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO role_professor;

-- Criação de um utilizador com as roles definidas
CREATE USER app_user WITH PASSWORD 'xoN924kot';

-- Atribuição das roles ao utilizador
GRANT role_estudante TO app_user;
GRANT role_professor TO app_user;

-- Conceder permissão de USAGE na sequência de utilizadores_id_seq para role_professor
GRANT USAGE ON SEQUENCE utilizadores_id_seq TO role_professor;

-- Conceder permissão de USAGE na sequência de utilizadores_id_seq para role_estudante
GRANT USAGE ON SEQUENCE utilizadores_id_seq TO role_estudante;

-- É uma boa prática conceder USAGE nas sequências para o app_user também,
-- pois ele é quem executa as operações diretamente.
GRANT USAGE ON SEQUENCE utilizadores_id_seq TO app_user;

-- Repita para outras sequências se aplicável (ex: aulas_id_seq, materiais_didaticos_id_seq, recomendacoes_id_seq)
GRANT USAGE ON SEQUENCE aulas_id_seq TO role_professor;
GRANT USAGE ON SEQUENCE aulas_id_seq TO role_estudante; -- Se estudantes forem listar aulas que foram criadas com IDs, eles também precisam de USAGE na sequence

-- E para as outras tables com SERIAL/BIGSERIAL
GRANT USAGE ON SEQUENCE materiais_didaticos_id_seq TO role_professor;
GRANT USAGE ON SEQUENCE materiais_didaticos_id_seq TO role_estudante; -- Se estudantes forem listar materiais

GRANT USAGE ON SEQUENCE recomendacoes_id_seq TO role_professor;
GRANT USAGE ON SEQUENCE recomendacoes_id_seq TO role_estudante; -- Se estudantes forem listar recomendações

-- E, crucialmente, para novas sequências criadas no futuro:
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public
GRANT USAGE ON SEQUENCES TO role_professor;

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public
GRANT USAGE ON SEQUENCES TO role_estudante;

-- E também para o app_user, se ele for o criador de objetos
ALTER DEFAULT PRIVILEGES FOR ROLE app_user IN SCHEMA public
GRANT USAGE ON SEQUENCES TO role_professor;

ALTER DEFAULT PRIVILEGES FOR ROLE app_user IN SCHEMA public
GRANT USAGE ON SEQUENCES TO role_estudante;

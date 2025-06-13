-- Função para criar um novo utilizador

CREATE OR REPLACE FUNCTION criar_utilizador(
    p_nome TEXT,
    p_email TEXT,
    p_password TEXT,
    p_tipo TEXT
)
RETURNS INT
AS $$
DECLARE
    novo_id INT;
BEGIN
    INSERT INTO utilizadores (nome, email, password, tipo_utilizador)
    VALUES (p_nome, p_email, p_password, p_tipo)
    RETURNING id INTO novo_id;

    IF p_tipo = 'estudante' THEN
        INSERT INTO estudantes_info (id_utilizador) VALUES (novo_id);
    ELSIF p_tipo = 'professor' THEN
        INSERT INTO professores_info (id_utilizador) VALUES (novo_id);
    END IF;

    RETURN novo_id;
END;
$$ LANGUAGE plpgsql;

-- Função para procurar um utilizador por email

CREATE OR REPLACE FUNCTION procurar_utilizador_por_email(p_email TEXT)
RETURNS TABLE (
    user_id INT,
    user_password TEXT,
    user_tipo_utilizador VARCHAR(20)
)
AS $$
BEGIN
    RETURN QUERY
    SELECT u.id, u.password, u.tipo_utilizador
    FROM utilizadores u
    WHERE u.email = p_email;
END;
$$ LANGUAGE plpgsql;

-- Função para criar uma nova aula, validando conflitos de horário

CREATE OR REPLACE FUNCTION criar_aula_bd(
    p_titulo TEXT,
    p_data DATE,
    p_hora_inicio TIME,
    p_hora_fim TIME,
    p_id_professor INT
)
RETURNS INT -- Vai retornar o ID da aula criada
LANGUAGE plpgsql
AS $$
DECLARE
    novo_id_aula INT;
    conflito_existe BOOLEAN;
BEGIN
    -- 1. Validar Conflito de Horário para o Professor
    -- O operador OVERLAPS já verifica se os intervalos de tempo se sobrepõem de alguma forma.
    -- Ele cobre os casos de um intervalo estar dentro do outro, ou se cruzarem parcialmente.
    SELECT EXISTS (
        SELECT 1
        FROM aulas
        WHERE
            id_professor = p_id_professor AND
            data = p_data AND
            (
                (p_hora_inicio, p_hora_fim) OVERLAPS (hora_inicio, hora_fim)
            )
    ) INTO conflito_existe;

    -- Se houver um conflito, levanta uma exceção
    IF conflito_existe THEN
        RAISE EXCEPTION 'Professor já tem uma aula agendada para o mesmo horário e dia.';
    END IF;

    -- 2. Inserir a Nova Aula se não houver conflito
    INSERT INTO aulas (titulo, data, hora_inicio, hora_fim, id_professor)
    VALUES (p_titulo, p_data, p_hora_inicio, p_hora_fim, p_id_professor)
    RETURNING id INTO novo_id_aula;

    RETURN novo_id_aula;
END;
$$;

-- Função para atualizar perfil de professor

CREATE OR REPLACE FUNCTION atualizar_area_especializacao_professor(
    p_id_professor INT,
    p_nova_area_especializacao VARCHAR
)
RETURNS VOID -- Não retorna nada, apenas executa a ação
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE professores_info
    SET area_especializacao = p_nova_area_especializacao
    WHERE id_utilizador = p_id_professor;
END;
$$;

-- Função para criar material didático
CREATE OR REPLACE FUNCTION criar_material_didatico_bd(
    p_titulo VARCHAR,
    p_tipo VARCHAR,
    p_autor VARCHAR,
    p_url TEXT,
    p_conteudo BYTEA
)
RETURNS INT
LANGUAGE plpgsql
AS $$
DECLARE
    novo_material_id INT;
BEGIN
    INSERT INTO materiais_didaticos (titulo, tipo, autor, url, conteudo)
    VALUES (p_titulo, p_tipo, p_autor, p_url, p_conteudo)
    RETURNING id INTO novo_material_id;
    RETURN novo_material_id;
END;
$$;

-- Função para recomendar material em aula
CREATE OR REPLACE FUNCTION recomendar_material_aula_bd(
    p_id_aula INT,
    p_id_material INT,
    p_id_professor INT,
    p_nota TEXT
)
RETURNS INT
LANGUAGE plpgsql
AS $$
DECLARE
    nova_recomendacao_id INT;
    v_data_aula DATE; -- Nova variável para armazenar a data da aula
BEGIN
    -- Obter a data da aula a partir do id_aula
    SELECT data INTO v_data_aula
    FROM aulas
    WHERE id = p_id_aula;

    -- Verificar se a aula existe (caso o ID seja inválido)
    IF v_data_aula IS NULL THEN
        RAISE EXCEPTION 'Aula com ID % não encontrada.', p_id_aula;
    END IF;

    -- Inserir na tabela de recomendacoes
    INSERT INTO recomendacoes (id_aula, data_aula, id_material, id_professor, nota)
    VALUES (p_id_aula, v_data_aula, p_id_material, p_id_professor, p_nota)
    RETURNING id INTO nova_recomendacao_id;

    RETURN nova_recomendacao_id;
END;
$$;
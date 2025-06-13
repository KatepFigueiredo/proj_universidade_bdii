-- Procedimento para matricular estudante em aula
CREATE OR REPLACE PROCEDURE matricular_estudante_aula(
    p_id_estudante INT,
    p_id_aula INT
    -- REMOVIDO p_data_aula da assinatura
)
LANGUAGE plpgsql
AS $$
DECLARE
    estudante_existe BOOLEAN;
    v_data_aula DATE; -- Nova variável para armazenar a data da aula
    ja_matriculado BOOLEAN;
BEGIN
    -- 1. Verificar se estudante existe e é do tipo 'estudante'
    SELECT EXISTS (
        SELECT 1 FROM utilizadores WHERE id = p_id_estudante AND tipo_utilizador = 'estudante'
    ) INTO estudante_existe;

    IF NOT estudante_existe THEN
        RAISE EXCEPTION 'Estudante com ID % não encontrado ou não é um estudante válido.', p_id_estudante;
    END IF;

    -- 2. Obter a data da aula a partir do id_aula e verificar se a aula existe
    SELECT data INTO v_data_aula
    FROM aulas
    WHERE id = p_id_aula;

    IF v_data_aula IS NULL THEN
        RAISE EXCEPTION 'Aula com ID % não encontrada.', p_id_aula;
    END IF;

    -- 3. Verificar se já está matriculado (usando a data obtida)
    SELECT EXISTS (
        SELECT 1 FROM participacoes WHERE id_estudante = p_id_estudante AND id_aula = p_id_aula AND data_aula = v_data_aula
    ) INTO ja_matriculado;

    IF ja_matriculado THEN
        RAISE EXCEPTION 'Estudante com ID % já está matriculado na aula % na data %.', p_id_estudante, p_id_aula, v_data_aula;
    END IF;

    -- 4. Inserir na tabela de participações
    INSERT INTO participacoes (id_estudante, id_aula, data_aula)
    VALUES (p_id_estudante, p_id_aula, v_data_aula);

    -- Não use COMMIT/ROLLBACK aqui, deixe para a aplicação Flask.
END;
$$;
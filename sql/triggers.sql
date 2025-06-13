CREATE OR REPLACE FUNCTION log_professor_update()
RETURNS TRIGGER AS $$
BEGIN
    -- Verifica se a área de especialização foi alterada
    IF OLD.area_especializacao IS DISTINCT FROM NEW.area_especializacao THEN
        INSERT INTO professor_log_atividades (id_professor, acao)
        VALUES (
            NEW.id_utilizador,
            'Área de especialização atualizada de "' || COALESCE(OLD.area_especializacao, '[NULO]') || '" para "' || COALESCE(NEW.area_especializacao, '[NULO]') || '"'
            -- ALTERADO: Adicionado COALESCE para tratar valores NULL
        );
    END IF;
    -- Adicionar mais condições para outros campos se existirem e quiser auditar
    RETURN NEW; -- Necessário para triggers AFTER UPDATE
END;
$$ LANGUAGE plpgsql;
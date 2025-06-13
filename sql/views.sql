-- View que exibe as aulas disponíveis ordenadas por data.

CREATE OR REPLACE VIEW aulas_disponiveis AS
SELECT
    id,
    titulo,
    data,
    hora_inicio,
    hora_fim,
    id_professor
FROM
    aulas
ORDER BY
    data DESC;

-- View para listar professores
CREATE OR REPLACE VIEW professores_universidade AS
SELECT
    u.id,
    u.nome,
    u.email,
    pi.area_especializacao
FROM
    utilizadores u
JOIN
    professores_info pi ON u.id = pi.id_utilizador
WHERE
    u.tipo_utilizador = 'professor'
ORDER BY
    u.nome;

-- View para listar recomendações de uma aula (usando parâmetros como filtros no SELECT no Flask)
-- Esta view lista todas as recomendações e a filtragem será feita no Flask para ter flexibilidade
CREATE OR REPLACE VIEW recomendacoes_detalhadas AS
SELECT
    r.id,
    r.id_aula,
    r.data_aula,
    md.titulo AS titulo_material,
    md.tipo AS tipo_material,
    md.autor AS autor_material,
    md.url AS url_material,
    r.nota,
    u.nome AS professor_nome
FROM
    recomendacoes r
JOIN
    materiais_didaticos md ON r.id_material = md.id
JOIN
    utilizadores u ON r.id_professor = u.id;

-- View para listar aulas assistidas por estudante
CREATE OR REPLACE VIEW aulas_assistidas_por_estudante AS
SELECT
    p.id_estudante,
    p.id_aula,
    p.data_aula,
    a.titulo AS titulo_aula,
    a.hora_inicio,
    a.hora_fim,
    up.nome AS professor_nome
FROM
    participacoes p
JOIN
    aulas a ON p.id_aula = a.id AND p.data_aula = a.data
JOIN
    utilizadores up ON a.id_professor = up.id;
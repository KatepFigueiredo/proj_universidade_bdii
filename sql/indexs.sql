CREATE INDEX IF NOT EXISTS ix_aulas_professor_data_horario ON aulas (id_professor, data, hora_inicio, hora_fim);
CREATE INDEX IF NOT EXISTS ix_participacoes_estudante ON participacoes (id_estudante);
CREATE INDEX IF NOT EXISTS ix_recomendacoes_aula_data ON recomendacoes (id_aula, data_aula);
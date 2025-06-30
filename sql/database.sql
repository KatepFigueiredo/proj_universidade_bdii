-- Tabela de Utilizadores
CREATE TABLE utilizadores (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    tipo_utilizador VARCHAR(20) NOT NULL CHECK (tipo_utilizador IN ('estudante', 'professor')),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de dados adicionais dos professores
CREATE TABLE professores_info (
    id_utilizador INT PRIMARY KEY REFERENCES utilizadores(id) ON DELETE CASCADE,
    area_especializacao VARCHAR(100)
);

-- Tabela de dados adicionais dos estudantes
CREATE TABLE estudantes_info (
    id_utilizador INT PRIMARY KEY REFERENCES utilizadores(id) ON DELETE CASCADE,
    data_nascimento DATE
);

-- Tabela de Aulas com partição por data
CREATE TABLE aulas (
    id SERIAL,
    titulo VARCHAR(100) NOT NULL,
    data DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fim TIME NOT NULL,
    id_professor INT NOT NULL,
    PRIMARY KEY (id, data),
    FOREIGN KEY (id_professor) REFERENCES utilizadores(id) ON DELETE CASCADE
) PARTITION BY RANGE (data);

-- Partições
CREATE TABLE aulas_2024 PARTITION OF aulas
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

CREATE TABLE aulas_2025 PARTITION OF aulas
    FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');

CREATE TABLE aulas_2026 PARTITION OF aulas
    FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');

-- Tabela Participações: Estudantes que assistiram a Aulas
CREATE TABLE participacoes (
    id_estudante INT,
    id_aula INT,
    data_aula DATE,
    PRIMARY KEY (id_estudante, id_aula),
    FOREIGN KEY (id_estudante) REFERENCES utilizadores(id) ON DELETE CASCADE,
    FOREIGN KEY (id_aula, data_aula) REFERENCES aulas(id, data) ON DELETE CASCADE
);

-- Tabela de Materiais Didáticos
CREATE TABLE materiais_didaticos (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    tipo VARCHAR(50) CHECK (tipo IN ('livro', 'artigo', 'video', 'slide')),
    autor VARCHAR(100),
    url TEXT,
	conteudo BYTEA
);

-- Recomendações de Materiais
CREATE TABLE recomendacoes (
    id SERIAL PRIMARY KEY,
    id_aula INT NOT NULL,
    data_aula DATE NOT NULL,
    id_material INT NOT NULL,
    id_professor INT NOT NULL,
    nota TEXT,
    FOREIGN KEY (id_aula, data_aula) REFERENCES aulas(id, data) ON DELETE CASCADE,
    FOREIGN KEY (id_material) REFERENCES materiais_didaticos(id) ON DELETE CASCADE,
    FOREIGN KEY (id_professor) REFERENCES utilizadores(id) ON DELETE SET NULL
);

CREATE TABLE professor_log_atividades (
    id SERIAL PRIMARY KEY,
    id_professor INT NOT NULL,
    acao TEXT NOT NULL,
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
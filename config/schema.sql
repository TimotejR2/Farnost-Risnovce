CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    nazov TEXT,
    obrazok TEXT,
    alt TEXT,
    datum TEXT,
    text TEXT,
    oblast INTEGER
);

CREATE TABLE IF NOT EXISTS sessions (
    session_id SERIAL PRIMARY KEY,
    user_id INTEGER,
    session VARCHAR(32),
    valid DATE,
    ip_address inet
);

CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    user_name VARCHAR(10),
    hash VARCHAR(64),
    level INTEGER
);

CREATE TABLE IF NOT EXISTS homilie (
    id SERIAL PRIMARY KEY,
    datum DATE,
    citanie TEXT,
    nazov TEXT,
    text TEXT
); 

CREATE TABLE IF NOT EXISTS oznamy (
    oznamy_id SERIAL PRIMARY KEY,
    list TEXT
);

CREATE TABLE IF NOT EXISTS wrong (
    id SERIAL PRIMARY KEY,
    cas TIMESTAMP
);

CREATE TABLE oznamy_tyzden (
    id SERIAL PRIMARY KEY,
    tyzden_zaciatok DATE NOT NULL,
    nadpis TEXT,                            -- napr. "Oznamy na 3. veľkonočnú nedeľu – 4.5.2025"
    popis TEXT                              -- očíslovaný viacreťazcový text (1.–8.)
);
CREATE TABLE oznamy_datum (
    id SERIAL PRIMARY KEY,
    tyzden_id INTEGER REFERENCES oznamy_tyzden(id) ON DELETE CASCADE,
    datum DATE NOT NULL,
    nazov VARCHAR(50)                       -- napr. "Vianoce", "Štedrý deň", voliteľné
);
CREATE TABLE oznamy_udalost (
    id SERIAL PRIMARY KEY,
    datum_id INTEGER REFERENCES oznamy_datum(id) ON DELETE CASCADE,
    cas TIME,
    miesto VARCHAR(30),
    popis TEXT
);
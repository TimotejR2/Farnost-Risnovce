CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    nazov TEXT,
    obrazok TEXT,
    alt TEXT,
    datum TEXT,
    text TEXT,
    autor TEXT DEFAULT 'Neznámy'
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
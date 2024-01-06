CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    nazov TEXT,
    obrazok TEXT,
    alt TEXT,
    datum TEXT,
    text TEXT,
    autor TEXT DEFAULT 'Neznámy'
);

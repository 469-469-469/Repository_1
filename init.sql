CREATE TABLE users (
    id UUID PRIMARY KEY,
    email TEXT NOT NULL,
    full_name TEXT,
    password TEXT NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    verified BOOLEAN,
    banned BOOLEAN,
    roles TEXT
);

CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    price NUMERIC,
    description TEXT,
    image_url TEXT,
    location TEXT,
    published BOOLEAN,
    genre_id INT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP
);
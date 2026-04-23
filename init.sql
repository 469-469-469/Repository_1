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
CREATE TABLE people (
    id SERIAL PRIMARY KEY,
    given_name VARCHAR(255),
    family_name VARCHAR(255),
    date_of_birth DATE,
    place_of_birth VARCHAR(255)
);

CREATE TABLE places (
    id SERIAL PRIMARY KEY,
    city VARCHAR(255),
    county VARCHAR(255),
    country VARCHAR(255)
);

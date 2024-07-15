-- Drop existing tables if they exist
DROP TABLE IF EXISTS people;
DROP TABLE IF EXISTS places;
DROP TABLE IF EXISTS people_temp;

-- Create the places table
CREATE TABLE places (
    id SERIAL PRIMARY KEY,
    city VARCHAR(255) UNIQUE,
    county VARCHAR(255),
    country VARCHAR(255)
);

-- Create the people table
CREATE TABLE people (
    id SERIAL PRIMARY KEY,
    given_name VARCHAR(255),
    family_name VARCHAR(255),
    date_of_birth DATE,
    place_of_birth INT,
    FOREIGN KEY (place_of_birth) REFERENCES places(id)
);

-- Create a temporary table for loading people data
CREATE TABLE people_temp (
    given_name VARCHAR(255),
    family_name VARCHAR(255),
    date_of_birth DATE,
    place_of_birth VARCHAR(255)
);

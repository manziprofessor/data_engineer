#!/usr/bin/env python

import csv
import json
import sqlalchemy
import time
import os

def load_csv_to_temp_table(file_path, table_name, engine):
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        with engine.connect() as connection:
            for row in reader:
                if table_name == 'people_temp':
                    connection.execute(sqlalchemy.text(
                        "INSERT INTO people_temp (given_name, family_name, date_of_birth, place_of_birth) VALUES (:1, :2, :3, :4)"
                    ), {'1': row[0], '2': row[1], '3': row[2], '4': row[3]})
                elif table_name == 'places':
                    connection.execute(sqlalchemy.text(
                        "INSERT INTO places (city, county, country) VALUES (:1, :2, :3) ON CONFLICT (city) DO NOTHING"
                    ), {'1': row[0], '2': row[1], '3': row[2]})

def migrate_people_data(engine):
    with engine.connect() as connection:
        connection.execute(sqlalchemy.text("""
            INSERT INTO people (given_name, family_name, date_of_birth, place_of_birth)
            SELECT pt.given_name, pt.family_name, pt.date_of_birth, p.id
            FROM people_temp pt
            JOIN places p ON pt.place_of_birth = p.city
        """))

def generate_summary_report(engine, output_file):
    with engine.connect() as connection:
        result = connection.execute(sqlalchemy.text("""
            SELECT p.country, COUNT(pe.id) as number_of_people
            FROM people pe
            JOIN places p ON pe.place_of_birth = p.id
            GROUP BY p.country;
        """))

        summary = {row[0]: row[1] for row in result}
    
        with open(output_file, 'w') as f:
            json.dump(summary, f, indent=4)

def connect_to_db():
    retries = 5
    while retries > 0:
        try:
            engine = sqlalchemy.create_engine(
                f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@db/{os.environ['POSTGRES_DB']}"
            )
            return engine
        except sqlalchemy.exc.OperationalError:
            retries -= 1
            print(f"Failed to connect to database. Retrying in 5 seconds... ({retries} retries left)")
            time.sleep(5)
    raise Exception("Could not connect to the database after several attempts")

def main():
    engine = connect_to_db()

    load_csv_to_temp_table('/data/people.csv', 'people_temp', engine)
    load_csv_to_temp_table('/data/places.csv', 'places', engine)
    migrate_people_data(engine)

    # Generate summary report and write to JSON file
    output_file = '/data/summary_report.json'
    generate_summary_report(engine, output_file)

if __name__ == '__main__':
    main()

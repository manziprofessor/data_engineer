import psycopg2
import time
import csv
import os
import json

def load_csv_to_temp_table(file_path, table_name, conn):
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        for row in reader:
            if table_name == 'people_temp':
                conn.cursor().execute(
                    "INSERT INTO people_temp (given_name, family_name, date_of_birth, place_of_birth) VALUES (%s, %s, %s, %s)", row)
            elif table_name == 'places':
                conn.cursor().execute(
                    "INSERT INTO places (city, county, country) VALUES (%s, %s, %s) ON CONFLICT (city) DO NOTHING", row)
        conn.commit()

def migrate_people_data(conn):
    conn.cursor().execute("""
        INSERT INTO people (given_name, family_name, date_of_birth, place_of_birth)
        SELECT pt.given_name, pt.family_name, pt.date_of_birth, p.id
        FROM people_temp pt
        JOIN places p ON pt.place_of_birth = p.city
    """)
    conn.commit()

def generate_summary_report(conn, output_file):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.country, COUNT(pe.id) as number_of_people
        FROM people pe
        JOIN places p ON pe.place_of_birth = p.id
        GROUP BY p.country;
    """)
    
    results = cursor.fetchall()
    summary = {row[0]: row[1] for row in results}
    
    with open(output_file, 'w') as f:
        json.dump(summary, f, indent=4)
    
    cursor.close()

def connect_to_db():
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(
                dbname=os.environ['POSTGRES_DB'],
                user=os.environ['POSTGRES_USER'],
                password=os.environ['POSTGRES_PASSWORD'],
                host='db'
            )
            return conn
        except psycopg2.OperationalError:
            retries -= 1
            print(f"Failed to connect to database. Retrying in 5 seconds... ({retries} retries left)")
            time.sleep(5)
    raise Exception("Could not connect to the database after several attempts")

def main():
    conn = connect_to_db()

    load_csv_to_temp_table('/data/people.csv', 'people_temp', conn)
    load_csv_to_temp_table('/data/places.csv', 'places', conn)
    migrate_people_data(conn)

    # Generate summary report and write to JSON file
    output_file = '/data/summary_report.json'
    generate_summary_report(conn, output_file)

    conn.close()

if __name__ == '__main__':
    main()

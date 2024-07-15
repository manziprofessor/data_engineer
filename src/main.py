import psycopg2
import csv
import os

def load_csv_to_db(file_path, table_name, conn):
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        for row in reader:
            if table_name == 'people':
                conn.cursor().execute(
                    "INSERT INTO people (given_name, family_name, date_of_birth, place_of_birth) VALUES (%s, %s, %s, %s)", row)
            elif table_name == 'places':
                conn.cursor().execute(
                    "INSERT INTO places (city, county, country) VALUES (%s, %s, %s)", row)
        conn.commit()

def main():
    conn = psycopg2.connect(
        dbname=os.environ['POSTGRES_DB'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        host='db'
    )

    load_csv_to_db('/data/people.csv', 'people', conn)
    load_csv_to_db('/data/places.csv', 'places', conn)

    conn.close()

if __name__ == '__main__':
    main()

import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="phonebook_db",
        user="postgres",
        password="122101"
    )
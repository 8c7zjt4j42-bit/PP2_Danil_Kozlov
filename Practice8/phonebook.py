from connect import get_connection

def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        phone VARCHAR(20)
    );
    """)

    conn.commit()
    cur.close()
    conn.close()


def search():
    pattern = input("Enter search: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def upsert():
    name = input("Name: ")
    phone = input("Phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
    conn.commit()

    cur.close()
    conn.close()


def bulk_insert():
    names = input("Names (comma): ").split(",")
    phones = input("Phones (comma): ").split(",")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL insert_many(%s, %s)", (names, phones))
    conn.commit()

    cur.close()
    conn.close()


def pagination():
    limit = int(input("Limit: "))
    offset = int(input("Offset: "))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM get_contacts(%s, %s)", (limit, offset))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def delete():
    value = input("Enter name or phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL delete_contact(%s)", (value,))
    conn.commit()

    cur.close()
    conn.close()


def menu():
    while True:
        print("\n1. Search")
        print("2. Add/Update")
        print("3. Bulk insert")
        print("4. Pagination")
        print("5. Delete")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            search()
        elif choice == "2":
            upsert()
        elif choice == "3":
            bulk_insert()
        elif choice == "4":
            pagination()
        elif choice == "5":
            delete()
        elif choice == "0":
            break


if __name__ == "__main__":
    create_table()
    menu()
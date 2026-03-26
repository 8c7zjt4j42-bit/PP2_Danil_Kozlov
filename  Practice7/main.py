import psycopg2
import csv
import os


conn = psycopg2.connect(
    host="localhost",
    database="phonebook_db",
    user="postgres",
    password="122101"
)

cur = conn.cursor()


cur.execute("""
CREATE TABLE IF NOT EXISTS phonebook (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL
);
""")
conn.commit()


def add_user():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    cur.execute(
        "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
        (name, phone)
    )
    conn.commit()
    print("User added")



def show_all():
    cur.execute("SELECT * FROM phonebook ORDER BY id ASC")
    rows = cur.fetchall()

    print("\n--- PhoneBook ---")
    for row in rows:
        print(row)



def search_user():
    name = input("Enter name to search: ")

    cur.execute(
        "SELECT * FROM phonebook WHERE name = %s",
        (name,)
    )

    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("User not found")



def search_by_name_part():
    part = input("Enter part of name: ")

    cur.execute(
        "SELECT * FROM phonebook WHERE name ILIKE %s",
        ("%" + part + "%",)
    )

    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No matches")



def search_by_prefix():
    prefix = input("Enter phone prefix: ")

    cur.execute(
        "SELECT * FROM phonebook WHERE phone LIKE %s",
        (prefix + "%",)
    )

    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No matches")



def update_user():
    name = input("Enter name to update: ")
    new_name = input("New name (press Enter to skip): ")
    new_phone = input("New phone (press Enter to skip): ")

    if new_name:
        cur.execute(
            "UPDATE phonebook SET name = %s WHERE name = %s",
            (new_name, name)
        )

    if new_phone:
        cur.execute(
            "UPDATE phonebook SET phone = %s WHERE name = %s",
            (new_phone, name)
        )

    conn.commit()
    print("Updated")



def delete_user():
    name = input("Enter name to delete: ")

    cur.execute(
        "DELETE FROM phonebook WHERE name = %s",
        (name,)
    )

    conn.commit()
    print("Deleted")



def insert_from_csv():
    try:
        file_path = os.path.join(os.path.dirname(__file__), "data.csv")

        with open(file_path, "r") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                cur.execute(
                    "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
                    (row[0], row[1])
                )

        conn.commit()
        print("CSV data inserted")

    except FileNotFoundError:
        print("data.csv not found")




while True:
    print("\n===== MENU =====")
    print("1. Add user")
    print("2. Show all users")
    print("3. Search user (exact)")
    print("4. Search by name (part)")
    print("5. Search by phone prefix")
    print("6. Update user")
    print("7. Delete user")
    print("8. Insert from CSV")
    print("9. Exit")

    choice = input("Choose: ")

    if choice == "1":
        add_user()

    elif choice == "2":
        show_all()

    elif choice == "3":
        search_user()

    elif choice == "4":
        search_by_name_part()

    elif choice == "5":
        search_by_prefix()

    elif choice == "6":
        update_user()

    elif choice == "7":
        delete_user()

    elif choice == "8":
        insert_from_csv()

    elif choice == "9":
        break

    else:
        print("Invalid choice")



cur.close()
conn.close()
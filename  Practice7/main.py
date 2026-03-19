import psycopg2
import csv


conn = psycopg2.connect(
    host="localhost",
    database="phonebook_db",
    user="postgres",
    password="122101"  
)

cur = conn.cursor()


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


def update_user():
    name = input("Enter name to update: ")
    new_phone = input("Enter new phone: ")

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
        with open("data.csv", "r") as file:
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
    print("3. Search user")
    print("4. Update user")
    print("5. Delete user")
    print("6. Insert from CSV")
    print("7. Exit")

    choice = input("Choose: ")

    if choice == "1":
        add_user()

    elif choice == "2":
        show_all()

    elif choice == "3":
        search_user()

    elif choice == "4":
        update_user()

    elif choice == "5":
        delete_user()

    elif choice == "6":
        insert_from_csv()

    elif choice == "7":
        break

    else:
        print("Invalid choice")



cur.close()
conn.close()
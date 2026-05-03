import json
import csv
from datetime import date, datetime
from connect import get_connection


def print_rows(rows):
    if not rows:
        print("No results.")
        return

    for row in rows:
        print(row)


def show_contacts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT pb.id, pb.name, pb.email, pb.birthday, g.name, ph.phone, ph.type, pb.created_at
        FROM phonebook pb
        LEFT JOIN groups g ON pb.group_id = g.id
        LEFT JOIN phones ph ON pb.id = ph.contact_id
        ORDER BY pb.id;
    """)

    rows = cur.fetchall()
    print_rows(rows)

    cur.close()
    conn.close()


def add_contact():
    name = input("Name: ")
    phone = input("Phone: ")
    phone_type = input("Phone type (home/work/mobile): ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group = input("Group (Family/Work/Friend/Other): ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO groups (name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING;
    """, (group,))

    cur.execute("SELECT id FROM groups WHERE name = %s;", (group,))
    group_id = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO phonebook (name, phone, email, birthday, group_id)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
    """, (name, phone, email, birthday, group_id))

    contact_id = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO phones (contact_id, phone, type)
        VALUES (%s, %s, %s);
    """, (contact_id, phone, phone_type))

    conn.commit()
    cur.close()
    conn.close()

    print("Contact added.")


def add_phone():
    name = input("Contact name: ")
    phone = input("New phone: ")
    phone_type = input("Type (home/work/mobile): ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL add_phone(%s, %s, %s);", (name, phone, phone_type))

    conn.commit()
    cur.close()
    conn.close()

    print("Phone added.")


def move_to_group():
    name = input("Contact name: ")
    group = input("New group: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL move_to_group(%s, %s);", (name, group))

    conn.commit()
    cur.close()
    conn.close()

    print("Contact moved.")


def search_contacts_console():
    query = input("Search text: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s);", (query,))
    rows = cur.fetchall()
    print_rows(rows)

    cur.close()
    conn.close()


def filter_by_group():
    group = input("Group name: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT pb.id, pb.name, pb.email, pb.birthday, g.name, ph.phone, ph.type
        FROM phonebook pb
        LEFT JOIN groups g ON pb.group_id = g.id
        LEFT JOIN phones ph ON pb.id = ph.contact_id
        WHERE g.name ILIKE %s
        ORDER BY pb.id;
    """, (group,))

    rows = cur.fetchall()
    print_rows(rows)

    cur.close()
    conn.close()


def search_by_email():
    email = input("Email search text: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, email, birthday
        FROM phonebook
        WHERE email ILIKE %s
        ORDER BY id;
    """, ("%" + email + "%",))

    rows = cur.fetchall()
    print_rows(rows)

    cur.close()
    conn.close()


def sort_contacts():
    print("1. Sort by name")
    print("2. Sort by birthday")
    print("3. Sort by date added")

    choice = input("Choose: ")

    allowed_fields = {
        "1": "name",
        "2": "birthday",
        "3": "created_at"
    }

    sort_field = allowed_fields.get(choice)

    if not sort_field:
        print("Invalid choice.")
        return

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f"""
        SELECT id, name, email, birthday, created_at
        FROM phonebook
        ORDER BY {sort_field};
    """)

    rows = cur.fetchall()
    print_rows(rows)

    cur.close()
    conn.close()


def paginated_contacts():
    limit = 3
    offset = 0

    while True:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, name, email, birthday, created_at
            FROM phonebook
            ORDER BY id
            LIMIT %s OFFSET %s;
        """, (limit, offset))

        rows = cur.fetchall()

        print("\n--- PAGE ---")
        print_rows(rows)

        cur.close()
        conn.close()

        command = input("next / prev / quit: ")

        if command == "next":
            offset += limit
        elif command == "prev":
            offset = max(0, offset - limit)
        elif command == "quit":
            break
        else:
            print("Invalid command.")


def export_to_json():
    filename = input("JSON filename to export: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT pb.id, pb.name, pb.email, pb.birthday, g.name
        FROM phonebook pb
        LEFT JOIN groups g ON pb.group_id = g.id
        ORDER BY pb.id;
    """)

    contacts = cur.fetchall()
    data = []

    for contact in contacts:
        contact_id, name, email, birthday, group_name = contact

        cur.execute("""
            SELECT phone, type
            FROM phones
            WHERE contact_id = %s;
        """, (contact_id,))

        phones = cur.fetchall()

        data.append({
            "name": name,
            "email": email,
            "birthday": birthday.isoformat() if birthday else None,
            "group": group_name,
            "phones": [
                {
                    "phone": phone,
                    "type": phone_type
                }
                for phone, phone_type in phones
            ]
        })

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    cur.close()
    conn.close()

    print("Export completed.")


def import_from_json():
    filename = input("JSON filename to import: ")

    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    conn = get_connection()
    cur = conn.cursor()

    for item in data:
        name = item["name"]
        email = item.get("email")
        birthday = item.get("birthday")
        group = item.get("group", "Other")
        phones = item.get("phones", [])

        cur.execute("SELECT id FROM phonebook WHERE name = %s LIMIT 1;", (name,))
        existing = cur.fetchone()

        if existing:
            action = input(f"Contact {name} exists. skip/overwrite: ")

            if action == "skip":
                continue

            if action == "overwrite":
                contact_id = existing[0]

                cur.execute("""
                    INSERT INTO groups (name)
                    VALUES (%s)
                    ON CONFLICT (name) DO NOTHING;
                """, (group,))

                cur.execute("SELECT id FROM groups WHERE name = %s;", (group,))
                group_id = cur.fetchone()[0]

                cur.execute("""
                    UPDATE phonebook
                    SET email = %s, birthday = %s, group_id = %s
                    WHERE id = %s;
                """, (email, birthday, group_id, contact_id))

                cur.execute("DELETE FROM phones WHERE contact_id = %s;", (contact_id,))
            else:
                print("Invalid action. Skipped.")
                continue
        else:
            cur.execute("""
                INSERT INTO groups (name)
                VALUES (%s)
                ON CONFLICT (name) DO NOTHING;
            """, (group,))

            cur.execute("SELECT id FROM groups WHERE name = %s;", (group,))
            group_id = cur.fetchone()[0]

            first_phone = phones[0]["phone"] if phones else None

            cur.execute("""
                INSERT INTO phonebook (name, phone, email, birthday, group_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;
            """, (name, first_phone, email, birthday, group_id))

            contact_id = cur.fetchone()[0]

        for phone_item in phones:
            cur.execute("""
                INSERT INTO phones (contact_id, phone, type)
                VALUES (%s, %s, %s);
            """, (contact_id, phone_item["phone"], phone_item["type"]))

    conn.commit()
    cur.close()
    conn.close()

    print("Import completed.")


def import_from_csv():
    filename = input("CSV filename to import: ")

    conn = get_connection()
    cur = conn.cursor()

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            name = row["name"]
            email = row.get("email")
            birthday = row.get("birthday")
            group = row.get("group", "Other")
            phone = row["phone"]
            phone_type = row.get("type", "mobile")

            cur.execute("""
                INSERT INTO groups (name)
                VALUES (%s)
                ON CONFLICT (name) DO NOTHING;
            """, (group,))

            cur.execute("SELECT id FROM groups WHERE name = %s;", (group,))
            group_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO phonebook (name, phone, email, birthday, group_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;
            """, (name, phone, email, birthday, group_id))

            contact_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO phones (contact_id, phone, type)
                VALUES (%s, %s, %s);
            """, (contact_id, phone, phone_type))

    conn.commit()
    cur.close()
    conn.close()

    print("CSV import completed.")


def menu():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Show contacts")
        print("2. Add contact")
        print("3. Add phone")
        print("4. Move to group")
        print("5. Search contacts")
        print("6. Filter by group")
        print("7. Search by email")
        print("8. Sort contacts")
        print("9. Paginated contacts")
        print("10. Export to JSON")
        print("11. Import from JSON")
        print("12. Import from CSV")
        print("13. Exit")

        choice = input("Choose: ")

        if choice == "1":
            show_contacts()
        elif choice == "2":
            add_contact()
        elif choice == "3":
            add_phone()
        elif choice == "4":
            move_to_group()
        elif choice == "5":
            search_contacts_console()
        elif choice == "6":
            filter_by_group()
        elif choice == "7":
            search_by_email()
        elif choice == "8":
            sort_contacts()
        elif choice == "9":
            paginated_contacts()
        elif choice == "10":
            export_to_json()
        elif choice == "11":
            import_from_json()
        elif choice == "12":
            import_from_csv()
        elif choice == "13":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()
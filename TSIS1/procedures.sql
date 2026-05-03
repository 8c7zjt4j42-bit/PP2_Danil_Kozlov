DROP FUNCTION IF EXISTS search_contacts(TEXT);

CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    SELECT id INTO v_contact_id
    FROM phonebook
    WHERE name = p_contact_name
    LIMIT 1;

    IF v_contact_id IS NULL THEN
        RAISE NOTICE 'Contact not found: %', p_contact_name;
        RETURN;
    END IF;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type);
END;
$$;


CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_group_id INTEGER;
BEGIN
    INSERT INTO groups (name)
    VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    SELECT id INTO v_group_id
    FROM groups
    WHERE name = p_group_name;

    UPDATE phonebook
    SET group_id = v_group_id
    WHERE name = p_contact_name;
END;
$$;


CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    contact_id INTEGER,
    contact_name VARCHAR,
    contact_email VARCHAR,
    contact_birthday DATE,
    group_name VARCHAR,
    phone_number VARCHAR,
    phone_type VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        pb.id,
        pb.name,
        pb.email,
        pb.birthday,
        g.name,
        ph.phone,
        ph.type
    FROM phonebook pb
    LEFT JOIN groups g ON pb.group_id = g.id
    LEFT JOIN phones ph ON pb.id = ph.contact_id
    WHERE 
        pb.name ILIKE '%' || p_query || '%'
        OR pb.email ILIKE '%' || p_query || '%'
        OR ph.phone ILIKE '%' || p_query || '%';
END;
$$;
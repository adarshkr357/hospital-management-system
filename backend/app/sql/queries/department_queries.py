GET_ALL_DEPARTMENTS_QUERY = """
    SELECT id, name, description, created_at, updated_at
    FROM departments
    ORDER BY name;
"""

GET_DEPARTMENT_BY_ID_QUERY = """
    SELECT id, name, description, created_at, updated_at
    FROM departments
    WHERE id = %s;
"""

CREATE_DEPARTMENT_QUERY = """
    INSERT INTO departments (name, description)
    VALUES (%s, %s)
    RETURNING id;
"""

UPDATE_DEPARTMENT_QUERY = """
    UPDATE departments
    SET name = %s,
        description = %s,
        updated_at = NOW()
    WHERE id = %s
    RETURNING id;
"""

GET_DEPARTMENT_STAFF_QUERY = """
    SELECT id, full_name, role, email, contact_number
    FROM staff
    WHERE department_id = %s;
"""

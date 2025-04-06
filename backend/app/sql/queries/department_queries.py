GET_ALL_DEPARTMENTS_QUERY = """
    SELECT id, name, head_staff_id, current_workload, required_staff, created_at
    FROM departments
    ORDER BY name;
"""

GET_DEPARTMENT_BY_ID_QUERY = """
    SELECT id, name, head_staff_id, current_workload, required_staff, created_at
    FROM departments
    WHERE id = %s;
"""

CREATE_DEPARTMENT_QUERY = """
    INSERT INTO departments (name, head_staff_id, required_staff)
    VALUES (%s, %s, %s)
    RETURNING id;
"""

UPDATE_DEPARTMENT_QUERY = """
    UPDATE departments
    SET name = %s,
        head_staff_id = %s,
        required_staff = %s
    WHERE id = %s
    RETURNING id;
"""

GET_DEPARTMENT_STAFF_QUERY = """
    SELECT s.id, s.full_name, s.role, u.email, s.contact_number
    FROM staff s
    JOIN users u ON s.user_id = u.id
    WHERE s.department_id = %s;
"""

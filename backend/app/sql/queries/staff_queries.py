GET_ALL_STAFF_QUERY = """
    SELECT s.*, d.name as department_name
    FROM staff s
    LEFT JOIN departments d ON s.department_id = d.id
    ORDER BY s.id;
"""

GET_STAFF_BY_ID_QUERY = """
    SELECT s.*, d.name as department_name
    FROM staff s
    LEFT JOIN departments d ON s.department_id = d.id
    WHERE s.id = %s;
"""

CREATE_STAFF_QUERY = """
    INSERT INTO staff (
        full_name, role, department_id, contact_number, 
        email, joining_date, qualifications, schedule
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id;
"""

UPDATE_STAFF_QUERY = """
    UPDATE staff
    SET full_name = %s,
        role = %s,
        department_id = %s,
        contact_number = %s,
        email = %s,
        qualifications = %s,
        schedule = %s,
        updated_at = NOW()
    WHERE id = %s
    RETURNING id;
"""

GET_STAFF_SCHEDULE_QUERY = """
    SELECT id, full_name, schedule
    FROM staff
    WHERE department_id = %s;
"""

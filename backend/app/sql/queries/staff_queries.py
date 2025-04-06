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
        user_id, department_id, full_name, role, specialization, contact_number
    )
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING id;
"""


UPDATE_STAFF_QUERY = """
    UPDATE staff
    SET full_name = %s,
        role = %s,
        department_id = %s,
        specialization = %s,
        contact_number = %s
    WHERE id = %s
    RETURNING id;
"""


GET_STAFF_SCHEDULE_QUERY = """
    SELECT s.id, s.full_name, ss.shift_start, ss.shift_end, ss.work_days, ss.is_overtime
    FROM staff s
    JOIN staff_schedules ss ON s.id = ss.staff_id
    WHERE s.department_id = %s;
"""


GET_ALL_STAFF_SCHEDULES_QUERY = """
    SELECT ss.id, ss.staff_id, s.full_name, ss.shift_start, ss.shift_end, ss.work_days, ss.is_overtime
    FROM staff_schedules ss
    JOIN staff s ON ss.staff_id = s.id
    ORDER BY ss.id;
"""
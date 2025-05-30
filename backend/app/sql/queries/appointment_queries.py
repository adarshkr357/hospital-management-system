GET_ALL_APPOINTMENTS_QUERY = """
    SELECT a.*, 
           p.full_name AS patient_name,
           s.full_name AS doctor_name
    FROM appointments a
    JOIN patients p ON a.patient_id = p.id
    JOIN staff s ON a.doctor_id = s.user_id
    ORDER BY a.appointment_date DESC;
"""

GET_APPOINTMENT_BY_ID_QUERY = """
    SELECT a.*, 
           p.full_name AS patient_name,
           s.full_name AS doctor_name
    FROM appointments a
    JOIN patients p ON a.patient_id = p.id
    JOIN staff s ON a.doctor_id = s.user_id
    WHERE a.id = %s;
"""

CREATE_APPOINTMENT_QUERY = """
    INSERT INTO appointments (
        patient_id, doctor_id, appointment_date, 
        status, purpose
    )
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id;
"""

UPDATE_APPOINTMENT_QUERY = """
    UPDATE appointments
    SET status = %s
    WHERE id = %s
    RETURNING id;
"""

GET_DOCTOR_APPOINTMENTS_QUERY = """
    SELECT a.*, p.full_name as patient_name
    FROM appointments a
    JOIN patients p ON a.patient_id = p.id
    WHERE a.doctor_id = %s AND a.appointment_date >= CURRENT_DATE
    ORDER BY a.appointment_date;
"""

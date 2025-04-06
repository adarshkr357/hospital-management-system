GET_ALL_PATIENTS_QUERY = """
    SELECT p.*, 
           COALESCE(json_agg(DISTINCT a) FILTER (WHERE a.id IS NOT NULL), '[]') AS allergy_details,
           COALESCE(json_agg(DISTINCT m) FILTER (WHERE m.id IS NOT NULL), '[]') AS medical_history_details
    FROM patients p
    LEFT JOIN patient_allergies a ON p.id = a.patient_id
    LEFT JOIN patient_medical_history m ON p.id = m.patient_id
    GROUP BY p.id
    ORDER BY p.id;
"""

GET_PATIENT_BY_ID_QUERY = """
    SELECT p.*, 
           COALESCE(json_agg(DISTINCT a) FILTER (WHERE a.id IS NOT NULL), '[]') AS allergy_details,
           COALESCE(json_agg(DISTINCT m) FILTER (WHERE m.id IS NOT NULL), '[]') AS medical_history_details
    FROM patients p
    LEFT JOIN patient_allergies a ON p.id = a.patient_id
    LEFT JOIN patient_medical_history m ON p.id = m.patient_id
    WHERE p.id = %s
    GROUP BY p.id;
"""

CREATE_PATIENT_QUERY = """
    INSERT INTO patients (
        user_id, full_name, date_of_birth, contact_number, emergency_contact, blood_group, allergies, current_medications
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id;
"""

UPDATE_PATIENT_QUERY = """
    UPDATE patients
    SET full_name = %s,
        date_of_birth = %s,
        contact_number = %s,
        emergency_contact = %s,
        blood_group = %s,
        allergies = %s,
        current_medications = %s
    WHERE id = %s
    RETURNING id;
"""

ADD_PATIENT_ALLERGY_QUERY = """
    INSERT INTO patient_allergies (
        patient_id, allergy_name, severity,
        diagnosed_date, notes
    )
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id;
"""

ADD_MEDICAL_HISTORY_QUERY = """
    INSERT INTO patient_medical_history (
        patient_id, condition, diagnosed_date,
        treatment, notes
    )
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id;
"""

GET_PATIENT_VISITS_QUERY = """
    SELECT a.*,
           s.full_name AS doctor_name,
           s.specialization
    FROM appointments a
    JOIN staff s ON a.doctor_id = s.user_id
    WHERE a.patient_id = %s
    ORDER BY a.appointment_date DESC;
"""

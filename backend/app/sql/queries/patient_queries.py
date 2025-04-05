GET_ALL_PATIENTS_QUERY = """
    SELECT p.*, 
           COALESCE(json_agg(DISTINCT a) FILTER (WHERE a.id IS NOT NULL), '[]') as allergies,
           COALESCE(json_agg(DISTINCT m) FILTER (WHERE m.id IS NOT NULL), '[]') as medical_history
    FROM patients p
    LEFT JOIN patient_allergies a ON p.id = a.patient_id
    LEFT JOIN patient_medical_history m ON p.id = m.patient_id
    GROUP BY p.id
    ORDER BY p.id;
"""

GET_PATIENT_BY_ID_QUERY = """
    SELECT p.*, 
           COALESCE(json_agg(DISTINCT a) FILTER (WHERE a.id IS NOT NULL), '[]') as allergies,
           COALESCE(json_agg(DISTINCT m) FILTER (WHERE m.id IS NOT NULL), '[]') as medical_history
    FROM patients p
    LEFT JOIN patient_allergies a ON p.id = a.patient_id
    LEFT JOIN patient_medical_history m ON p.id = m.patient_id
    WHERE p.id = %s
    GROUP BY p.id;
"""

CREATE_PATIENT_QUERY = """
    INSERT INTO patients (
        full_name, date_of_birth, gender, blood_group,
        contact_number, email, address, emergency_contact_name,
        emergency_contact_number, insurance_provider,
        insurance_id, created_at
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
    RETURNING id;
"""

UPDATE_PATIENT_QUERY = """
    UPDATE patients
    SET full_name = %s,
        contact_number = %s,
        email = %s,
        address = %s,
        emergency_contact_name = %s,
        emergency_contact_number = %s,
        insurance_provider = %s,
        insurance_id = %s,
        updated_at = NOW()
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
    SELECT v.*,
           d.full_name as doctor_name,
           d.specialization
    FROM patient_visits v
    JOIN staff d ON v.doctor_id = d.id
    WHERE v.patient_id = %s
    ORDER BY v.visit_date DESC;
"""

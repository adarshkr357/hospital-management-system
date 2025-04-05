GET_ALL_ADMISSIONS_QUERY = """
    SELECT a.*, 
           p.full_name as patient_name,
           p.contact_number
    FROM admissions a
    JOIN patients p ON a.patient_id = p.id
    ORDER BY a.admission_date DESC;
"""

GET_ADMISSION_BY_ID_QUERY = """
    SELECT a.*, 
           p.full_name as patient_name,
           p.contact_number
    FROM admissions a
    JOIN patients p ON a.patient_id = p.id
    WHERE a.id = %s;
"""

CREATE_ADMISSION_QUERY = """
    INSERT INTO admissions (
        patient_id, bed_number, admission_date,
        expected_discharge_date, status, notes
    )
    VALUES (%s, %s, %s, %s, 'ADMITTED', %s)
    RETURNING id;
"""

UPDATE_ADMISSION_QUERY = """
    UPDATE admissions
    SET status = %s,
        actual_discharge_date = CASE 
            WHEN %s = 'DISCHARGED' THEN NOW()
            ELSE actual_discharge_date
        END,
        discharge_summary = %s,
        updated_at = NOW()
    WHERE id = %s
    RETURNING id;
"""

GET_AVAILABLE_BEDS_QUERY = """
    SELECT bed_number, status
    FROM beds
    WHERE status = 'AVAILABLE'
    ORDER BY bed_number;
"""

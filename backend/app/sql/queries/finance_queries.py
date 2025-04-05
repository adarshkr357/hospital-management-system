GET_ALL_BILLS_QUERY = """
    SELECT b.*, 
           p.full_name as patient_name,
           p.contact_number
    FROM bills b
    JOIN patients p ON b.patient_id = p.id
    ORDER BY b.generated_date DESC;
"""

GET_BILL_BY_ID_QUERY = """
    SELECT b.*, 
           p.full_name as patient_name,
           p.contact_number
    FROM bills b
    JOIN patients p ON b.patient_id = p.id
    WHERE b.id = %s;
"""

CREATE_BILL_QUERY = """
    INSERT INTO bills (
        patient_id, admission_id, amount,
        generated_date, due_date, status
    )
    VALUES (%s, %s, %s, NOW(), %s, 'PENDING')
    RETURNING id;
"""

UPDATE_BILL_STATUS_QUERY = """
    UPDATE bills
    SET status = %s,
        payment_method = %s,
        updated_at = NOW()
    WHERE id = %s
    RETURNING id;
"""

GET_REVENUE_REPORT_QUERY = """
    SELECT 
        SUM(CASE WHEN generated_date::date = CURRENT_DATE 
            THEN amount ELSE 0 END) as daily_revenue,
        SUM(CASE WHEN generated_date >= date_trunc('month', CURRENT_DATE)
            THEN amount ELSE 0 END) as monthly_revenue,
        SUM(CASE WHEN status = 'PENDING' OR status = 'OVERDUE'
            THEN amount ELSE 0 END) as outstanding_amount
    FROM bills;
"""

GET_INSURANCE_CLAIMS_QUERY = """
    SELECT ic.*, 
           p.full_name as patient_name,
           b.amount as bill_amount
    FROM insurance_claims ic
    JOIN patients p ON ic.patient_id = p.id
    JOIN bills b ON ic.bill_id = b.id
    ORDER BY ic.submission_date DESC;
"""

CREATE_INSURANCE_CLAIM_QUERY = """
    INSERT INTO insurance_claims (
        patient_id, bill_id, insurance_provider,
        claim_amount, status, submission_date
    )
    VALUES (%s, %s, %s, %s, 'SUBMITTED', NOW())
    RETURNING id;
"""

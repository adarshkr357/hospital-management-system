# app/config/database.py
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from typing import Generator
import logging
from .settings import settings

logger = logging.getLogger(__name__)

# SQL statements for table creation
CREATE_TABLES_QUERIES = [
    """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        role VARCHAR(50) NOT NULL CHECK (role IN ('ADMIN', 'PATIENT', 'STAFF', 'FINANCE')),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS patients (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        full_name VARCHAR(255) NOT NULL,
        date_of_birth DATE NOT NULL,
        contact_number VARCHAR(20) NOT NULL,
        emergency_contact VARCHAR(20) NOT NULL,
        blood_group VARCHAR(5),
        allergies TEXT,
        current_medications TEXT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS patient_allergies (
        id SERIAL PRIMARY KEY,
        patient_id INTEGER REFERENCES patients(id),
        allergy_name VARCHAR(255) NOT NULL,
        severity VARCHAR(50),
        diagnosed_date DATE,
        notes TEXT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS patient_medical_history (
        id SERIAL PRIMARY KEY,
        patient_id INTEGER REFERENCES patients(id),
        condition VARCHAR(255) NOT NULL,
        diagnosed_date DATE,
        treatment TEXT,
        notes TEXT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS medical_records (
        id SERIAL PRIMARY KEY,
        patient_id INTEGER REFERENCES patients(id),
        diagnosis TEXT,
        treatment TEXT,
        prescription TEXT,
        test_results TEXT,
        doctor_notes TEXT,
        record_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS appointments (
        id SERIAL PRIMARY KEY,
        patient_id INTEGER REFERENCES patients(id),
        doctor_id INTEGER REFERENCES users(id),
        appointment_date TIMESTAMP NOT NULL,
        status VARCHAR(50) CHECK (status IN ('SCHEDULED', 'COMPLETED', 'CANCELLED', 'NO_SHOW')),
        purpose TEXT,
        reminder_sent BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS admissions (
        id SERIAL PRIMARY KEY,
        patient_id INTEGER REFERENCES patients(id),
        bed_number VARCHAR(10) NOT NULL,
        admission_date TIMESTAMP NOT NULL,
        expected_discharge_date TIMESTAMP,
        actual_discharge_date TIMESTAMP,
        status VARCHAR(50) CHECK (status IN ('ADMITTED', 'DISCHARGED')),
        discharge_summary TEXT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS departments (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        head_staff_id INTEGER REFERENCES users(id),
        current_workload INTEGER DEFAULT 0,
        required_staff INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS staff (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        department_id INTEGER REFERENCES departments(id),
        full_name VARCHAR(255) NOT NULL,
        role VARCHAR(50) CHECK (role IN ('DOCTOR', 'NURSE', 'ADMIN_STAFF')),
        specialization VARCHAR(100),
        contact_number VARCHAR(20)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS staff_schedules (
        id SERIAL PRIMARY KEY,
        staff_id INTEGER REFERENCES staff(id),
        shift_start TIME NOT NULL,
        shift_end TIME NOT NULL,
        work_days VARCHAR(20)[],
        is_overtime BOOLEAN DEFAULT FALSE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS attendance (
        id SERIAL PRIMARY KEY,
        staff_id INTEGER REFERENCES staff(id),
        date DATE NOT NULL,
        clock_in TIMESTAMP,
        clock_out TIMESTAMP,
        status VARCHAR(20) CHECK (status IN ('PRESENT', 'ABSENT', 'LEAVE', 'HALF_DAY')),
        overtime_hours DECIMAL(4,2) DEFAULT 0
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS leaves (
        id SERIAL PRIMARY KEY,
        staff_id INTEGER REFERENCES staff(id),
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        leave_type VARCHAR(50),
        status VARCHAR(20) CHECK (status IN ('PENDING', 'APPROVED', 'REJECTED')),
        reason TEXT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS bills (
        id SERIAL PRIMARY KEY,
        patient_id INTEGER REFERENCES patients(id),
        admission_id INTEGER REFERENCES admissions(id),
        amount DECIMAL(10,2) NOT NULL,
        generated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        due_date TIMESTAMP NOT NULL,
        status VARCHAR(20) CHECK (status IN ('PAID', 'PENDING', 'OVERDUE')),
        payment_method VARCHAR(50)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS insurance_claims (
        id SERIAL PRIMARY KEY,
        patient_id INTEGER REFERENCES patients(id),
        bill_id INTEGER REFERENCES bills(id),
        insurance_provider VARCHAR(100),
        claim_amount DECIMAL(10,2),
        submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status VARCHAR(20) CHECK (status IN ('SUBMITTED', 'APPROVED', 'REJECTED', 'PENDING')),
        rejection_reason TEXT,
        settlement_date TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS revenue (
        id SERIAL PRIMARY KEY,
        date DATE NOT NULL,
        department_id INTEGER REFERENCES departments(id),
        amount DECIMAL(10,2) NOT NULL,
        type VARCHAR(20) CHECK (type IN ('DAILY', 'MONTHLY')),
        source VARCHAR(50)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS notifications (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        type VARCHAR(50) CHECK (type IN ('APPOINTMENT', 'BILL', 'SHIFT_CHANGE', 'LEAVE_STATUS', 'OVERTIME')),
        message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        read BOOLEAN DEFAULT FALSE
    );
    """
]


@contextmanager
def get_db_connection() -> Generator:
    """Context manager for database connection"""
    conn = None
    try:
        conn = psycopg2.connect(
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            database=settings.DB_NAME,
            cursor_factory=RealDictCursor,
        )
        yield conn
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise
    finally:
        if conn is not None:
            conn.close()


@contextmanager
def get_db_cursor() -> Generator:
    """Context manager for database cursor"""
    with get_db_connection() as conn:
        cur = conn.cursor()
        try:
            yield cur
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database operation error: {e}")
            raise
        finally:
            cur.close()


def initialize_database():
    """Initialize database by creating all required tables"""
    try:
        with get_db_cursor() as cursor:
            for query in CREATE_TABLES_QUERIES:
                cursor.execute(query)
            logger.info("Database tables created successfully")
            return True
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        return False


def test_connection() -> bool:
    """Test database connection"""
    try:
        with get_db_connection() as conn:
            return True
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False

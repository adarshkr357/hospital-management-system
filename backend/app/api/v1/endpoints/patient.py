from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from ....core.security import get_current_user, check_permissions
from ....utils.db_utils import execute_query
from ....utils.validators import validate_email, validate_phone
from ....sql.queries.patient_queries import *

router = APIRouter()


@router.get("/")
async def get_all_patients(
    search: Optional[str] = None, current_user: dict = Depends(get_current_user)
):
    """Get all patients with optional search"""
    try:
        query = GET_ALL_PATIENTS_QUERY
        params = []

        if search:
            query = query.replace(
                "GROUP BY",
                "WHERE p.full_name ILIKE %s OR p.contact_number LIKE %s GROUP BY",
            )
            search_term = f"%{search}%"
            params.extend([search_term, search_term])

        patients = execute_query(query, tuple(params), fetch_all=True)
        return patients
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{patient_id}")
async def get_patient(patient_id: int, current_user: dict = Depends(get_current_user)):
    """Get specific patient details"""
    patient = execute_query(
        GET_PATIENT_BY_ID_QUERY, (patient_id,), fetch_one=True
    )
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.post("/")
async def create_patient(
    patient_data: dict,
    current_user: dict = Depends(check_permissions(["ADMIN", "STAFF", "FINANCE"])),
):
    """Create new patient"""
    # Validate email and phone
    if not validate_email(patient_data["email"]):
        raise HTTPException(status_code=400, detail="Invalid email format")
    if not validate_phone(patient_data["contact_number"]):
        raise HTTPException(status_code=400, detail="Invalid phone number")

    try:
        result = execute_query(
            CREATE_PATIENT_QUERY,
            (
                patient_data["full_name"],
                patient_data["date_of_birth"],
                patient_data["gender"],
                patient_data["blood_group"],
                patient_data["contact_number"],
                patient_data["email"],
                patient_data["address"],
                patient_data["emergency_contact_name"],
                patient_data["emergency_contact_number"],
                patient_data.get("insurance_provider"),
                patient_data.get("insurance_id"),
            ),
            fetch_one=True,
        )
        return {"message": "Patient created successfully", "patient_id": result["id"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{patient_id}")
async def update_patient(
    patient_id: int,
    patient_data: dict,
    current_user: dict = Depends(check_permissions(["ADMIN", "STAFF", "FINANCE"])),
):
    """Update patient information"""
    try:
        result = execute_query(
            UPDATE_PATIENT_QUERY,
            (
                patient_data["full_name"],
                patient_data["contact_number"],
                patient_data["email"],
                patient_data["address"],
                patient_data["emergency_contact_name"],
                patient_data["emergency_contact_number"],
                patient_data.get("insurance_provider"),
                patient_data.get("insurance_id"),
                patient_id,
            ),
            fetch_one=True,
        )
        if not result:
            raise HTTPException(status_code=404, detail="Patient not found")
        return {"message": "Patient updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{patient_id}/allergies")
async def add_patient_allergy(
    patient_id: int,
    allergy_data: dict,
    current_user: dict = Depends(check_permissions(["ADMIN", "STAFF", "FINANCE"])),
):
    """Add patient allergy"""
    try:
        result = execute_query(
            ADD_PATIENT_ALLERGY_QUERY,
            (
                patient_id,
                allergy_data["allergy_name"],
                allergy_data["severity"],
                allergy_data["diagnosed_date"],
                allergy_data.get("notes", ""),
            ),
            fetch_one=True,
        )
        return {"message": "Allergy added successfully", "allergy_id": result["id"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{patient_id}/medical-history")
async def add_medical_history(
    patient_id: int,
    history_data: dict,
    current_user: dict = Depends(check_permissions(["ADMIN", "STAFF", "FINANCE"])),
):
    """Add medical history entry"""
    try:
        result = execute_query(
            ADD_MEDICAL_HISTORY_QUERY,
            (
                patient_id,
                history_data["condition"],
                history_data["diagnosed_date"],
                history_data["treatment"],
                history_data.get("notes", ""),
            ),
            fetch_one=True,
        )
        return {
            "message": "Medical history added successfully",
            "history_id": result["id"],
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{patient_id}/visits")
async def get_patient_visits(
    patient_id: int, current_user: dict = Depends(get_current_user)
):
    """Get patient visit history"""
    try:
        visits = execute_query(
            GET_PATIENT_VISITS_QUERY, (patient_id,), fetch_all=True
        )
        return visits
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{patient_id}/visits")
async def record_patient_visit(
    patient_id: int,
    visit_data: dict,
    current_user: dict = Depends(check_permissions(["ADMIN", "STAFF", "FINANCE"])),
):
    """Record new patient visit"""
    try:
        result = execute_query(
            """
            INSERT INTO patient_visits (
                patient_id, doctor_id, visit_date,
                symptoms, diagnosis, prescription,
                notes
            )
            VALUES (%s, %s, NOW(), %s, %s, %s, %s)
            RETURNING id;
            """,
            (
                patient_id,
                visit_data["doctor_id"],
                visit_data["symptoms"],
                visit_data["diagnosis"],
                visit_data["prescription"],
                visit_data.get("notes", ""),
            ),
            fetch_one=True,
        )
        return {"message": "Visit recorded successfully", "visit_id": result["id"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

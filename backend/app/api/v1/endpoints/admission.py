from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime, date
from ....core.security import get_current_user, check_permissions
from ....utils.db_utils import execute_query
from ....utils.date_utils import validate_date_range
from ....sql.queries.admission_queries import *

router = APIRouter()


@router.get("/")
async def get_all_admissions(
    status: Optional[str] = None, current_user: dict = Depends(get_current_user)
):
    """Get all admissions"""
    try:
        query = GET_ALL_ADMISSIONS_QUERY
        params = []

        if status:
            query = query.replace("ORDER BY", f"WHERE a.status = %s ORDER BY")
            params.append(status)

        admissions = execute_query(query, tuple(params), fetch_all=True)
        return admissions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/")
async def create_admission(
    admission_data: dict,
    current_user: dict = Depends(check_permissions(["ADMIN", "DOCTOR"])),
):
    """Create new admission"""
    try:
        # Check bed availability
        available_beds = execute_query(GET_AVAILABLE_BEDS_QUERY, fetch_all=True)
        if not available_beds:
            raise HTTPException(status_code=400, detail="No beds available")

        result = execute_query(
            CREATE_ADMISSION_QUERY,
            (
                admission_data["patient_id"],
                admission_data["bed_number"],
                admission_data["admission_date"],
                admission_data["expected_discharge_date"],
                admission_data.get("notes", ""),
            ),
            fetch_one=True,
        )

        # Update bed status
        # TODO: Implement bed status update

        return {
            "message": "Admission created successfully",
            "admission_id": result["id"],
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{admission_id}/discharge")
async def discharge_patient(
    admission_id: int,
    discharge_data: dict,
    current_user: dict = Depends(check_permissions(["ADMIN", "DOCTOR"])),
):
    """Discharge patient"""
    try:
        execute_query(
            UPDATE_ADMISSION_QUERY,
            (
                "DISCHARGED",
                "DISCHARGED",
                discharge_data.get("discharge_summary", ""),
                admission_id,
            ),
        )

        # Update bed status
        # TODO: Implement bed status update

        return {"message": "Patient discharged successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/beds/available")
async def get_available_beds(current_user: dict = Depends(get_current_user)):
    """Get available beds"""
    beds = execute_query(GET_AVAILABLE_BEDS_QUERY, fetch_all=True)
    return beds

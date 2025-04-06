from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime, date
from ....core.security import get_current_user, check_permissions
from ....utils.db_utils import execute_query
from ....utils.date_utils import validate_date_range
from ....sql.queries.appointment_queries import *

router = APIRouter()


@router.get("/")
async def get_all_appointments(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    status: Optional[str] = None,
    current_user: dict = Depends(get_current_user),
):
    """Get all appointments with optional filters"""
    try:
        query = GET_ALL_APPOINTMENTS_QUERY
        params = []

        if start_date and end_date:
            if not validate_date_range(start_date, end_date):
                raise HTTPException(status_code=400, detail="Invalid date range")
            query = query.replace(
                "ORDER BY", f"WHERE a.appointment_date BETWEEN %s AND %s ORDER BY"
            )
            params.extend([start_date, end_date])

        if status:
            query = query.replace("ORDER BY", f"WHERE a.status = %s ORDER BY")
            params.append(status)

        appointments = execute_query(query, tuple(params), fetch_all=True)
        return appointments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/")
async def create_appointment(
    appointment_data: dict,
    current_user: dict = Depends(check_permissions(["ADMIN", "DOCTOR", "STAFF"])),
):
    """Create new appointment"""
    try:
        result = execute_query(
            CREATE_APPOINTMENT_QUERY,
            (
                appointment_data["patient_id"],
                appointment_data["doctor_id"],
                appointment_data["appointment_date"],
                "SCHEDULED",
                appointment_data["purpose"],
                appointment_data.get("notes", ""),
            ),
            fetch_one=True,
        )

        # Send notification to patient and doctor
        # TODO: Implement notification system

        return {
            "message": "Appointment created successfully",
            "appointment_id": result["id"],
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{appointment_id}")
async def update_appointment_status(
    appointment_id: int,
    status: str,
    notes: Optional[str] = None,
    current_user: dict = Depends(check_permissions(["ADMIN", "DOCTOR"])),
):
    """Update appointment status"""
    valid_statuses = ["SCHEDULED", "COMPLETED", "CANCELLED", "NO_SHOW"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}",
        )

    try:
        execute_query(UPDATE_APPOINTMENT_QUERY, (status, notes, appointment_id))
        return {"message": "Appointment updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/doctor/{doctor_id}")
async def get_doctor_appointments(
    doctor_id: int, current_user: dict = Depends(get_current_user)
):
    """Get all appointments for a specific doctor"""
    appointments = execute_query(
        GET_DOCTOR_APPOINTMENTS_QUERY, (doctor_id,), fetch_all=True
    )
    return appointments

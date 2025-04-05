from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from ....core.security import get_current_user, check_permissions
from ....utils.db_utils import execute_query
from ....utils.validators import validate_email, validate_phone
from ....sql.queries.staff_queries import *

router = APIRouter()


@router.get("/", response_model=List[dict])
async def get_all_staff(
    department_id: Optional[int] = None,
    role: Optional[str] = None,
    current_user: dict = Depends(check_permissions(["ADMIN", "HR"])),
):
    """Get all staff members with optional filtering"""
    try:
        query = GET_ALL_STAFF_QUERY
        params = []

        if department_id:
            query = query.replace(";", " WHERE s.department_id = %s;")
            params.append(department_id)
        if role:
            query = query.replace(";", " WHERE s.role = %s;")
            params.append(role)

        staff = await execute_query(query, tuple(params), fetch_all=True)
        return staff
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{staff_id}")
async def get_staff_member(
    staff_id: int, current_user: dict = Depends(check_permissions(["ADMIN", "HR"]))
):
    """Get specific staff member details"""
    staff = await execute_query(GET_STAFF_BY_ID_QUERY, (staff_id,), fetch_one=True)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff member not found")
    return staff


@router.post("/")
async def create_staff_member(
    staff_data: dict, current_user: dict = Depends(check_permissions(["ADMIN", "HR"]))
):
    """Create new staff member"""
    # Validate email and phone
    if not validate_email(staff_data["email"]):
        raise HTTPException(status_code=400, detail="Invalid email format")
    if not validate_phone(staff_data["contact_number"]):
        raise HTTPException(status_code=400, detail="Invalid phone number")

    try:
        result = await execute_query(
            CREATE_STAFF_QUERY,
            (
                staff_data["full_name"],
                staff_data["role"],
                staff_data["department_id"],
                staff_data["contact_number"],
                staff_data["email"],
                staff_data["joining_date"],
                staff_data["qualifications"],
                staff_data["schedule"],
            ),
            fetch_one=True,
        )
        return {
            "message": "Staff member created successfully",
            "staff_id": result["id"],
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{staff_id}")
async def update_staff_member(
    staff_id: int,
    staff_data: dict,
    current_user: dict = Depends(check_permissions(["ADMIN", "HR"])),
):
    """Update staff member details"""
    if not await execute_query(GET_STAFF_BY_ID_QUERY, (staff_id,), fetch_one=True):
        raise HTTPException(status_code=404, detail="Staff member not found")

    try:
        await execute_query(
            UPDATE_STAFF_QUERY,
            (
                staff_data["full_name"],
                staff_data["role"],
                staff_data["department_id"],
                staff_data["contact_number"],
                staff_data["email"],
                staff_data["qualifications"],
                staff_data["schedule"],
                staff_id,
            ),
        )
        return {"message": "Staff member updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/department/{department_id}/schedule")
async def get_department_schedule(
    department_id: int,
    current_user: dict = Depends(check_permissions(["ADMIN", "HR", "DOCTOR", "NURSE"])),
):
    """Get staff schedule for a specific department"""
    schedules = await execute_query(
        GET_STAFF_SCHEDULE_QUERY, (department_id,), fetch_all=True
    )
    return schedules

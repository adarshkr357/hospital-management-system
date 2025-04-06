from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from ....core.security import get_current_user, check_permissions
from ....utils.db_utils import execute_query
from ....utils.validators import validate_email, validate_phone
from ....sql.queries.staff_queries import *
  
router = APIRouter()

# Query for attendance
GET_ATTENDANCE_QUERY = """
    SELECT id, staff_id, date, clock_in, clock_out, status, overtime_hours
    FROM attendance
    WHERE staff_id = %s
    ORDER BY date DESC;
"""

# Output models
class StaffScheduleOut(BaseModel):
    id: int
    staff_id: int
    full_name: str
    shift_start: datetime
    shift_end: datetime
    work_days: List[str]
    is_overtime: bool

class AttendanceOut(BaseModel):
    id: int
    staff_id: int
    date: datetime
    clock_in: datetime
    clock_out: Optional[datetime]
    status: str
    overtime_hours: Optional[float]

# GET / -> Get all staff members with optional filtering by department and/or role.
@router.get("/", response_model=List[dict])
async def get_all_staff(
    department_id: Optional[int] = None,
    role: Optional[str] = None,
    current_user: dict = Depends(check_permissions(["ADMIN", "STAFF", "FINANCE"]))
):
    try:
        # Build the query dynamically
        query = GET_ALL_STAFF_QUERY.rstrip(";")
        params = []
        conditions = []
        if department_id:
            conditions.append("s.department_id = %s")
            params.append(department_id)
        if role:
            conditions.append("s.role = %s")
            params.append(role)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += ";"
        
        staff = execute_query(query, tuple(params), fetch_all=True)
        return staff
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Attendance endpoint: GET /attendance returns attendance records for given staff_id.
@router.get("/attendance", response_model=List[AttendanceOut])
def get_attendance_records(
    staff_id: Optional[int] = None,
    current_user: dict = Depends(get_current_user)
):
    # If staff_id is not provided, use the id from current_user
    if staff_id is None:
        staff_id = current_user.get("id")
    records = execute_query(GET_ATTENDANCE_QUERY, (staff_id,), fetch_all=True)
    return records



# Staff schedule endpoint: GET /schedule returns list of staff schedules.
@router.get("/schedule", response_model=List[StaffScheduleOut])
def get_all_staff_schedules(
    current_user: dict = Depends(get_current_user)
):
    schedules = execute_query(GET_ALL_STAFF_SCHEDULES_QUERY, fetch_all=True)
    if schedules is None:
        raise HTTPException(status_code=404, detail="No schedules found")
    return schedules


# GET /{staff_id} returns details for a specific staff member.
@router.get("/{staff_id}")
async def get_staff_member(
    staff_id: int,
    current_user: dict = Depends(check_permissions(["ADMIN", "STAFF", "FINANCE"]))
):
    staff = execute_query(GET_STAFF_BY_ID_QUERY, (staff_id,), fetch_one=True)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff member not found")
    return staff


# POST / -> Create a new staff member.
@router.post("/")
async def create_staff_member(
    staff_data: dict,
    current_user: dict = Depends(check_permissions(["ADMIN", "STAFF", "FINANCE"]))
):
    # Validate email and phone
    if not validate_email(staff_data["email"]):
        raise HTTPException(status_code=400, detail="Invalid email format")
    if not validate_phone(staff_data["contact_number"]):
        raise HTTPException(status_code=400, detail="Invalid phone number")
    
    try:
        result = execute_query(
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


# PUT /{staff_id} -> Update staff member details.
@router.put("/{staff_id}")
async def update_staff_member(
    staff_id: int,
    staff_data: dict,
    current_user: dict = Depends(check_permissions(["ADMIN", "STAFF", "FINANCE"]))
):
    if not execute_query(GET_STAFF_BY_ID_QUERY, (staff_id,), fetch_one=True):
        raise HTTPException(status_code=404, detail="Staff member not found")

    try:
        execute_query(
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


# GET /department/{department_id}/schedule -> Get schedule for a specific department.
@router.get("/department/{department_id}/schedule")
async def get_department_schedule(
    department_id: int,
    current_user: dict = Depends(check_permissions(["ADMIN"]))
):
    schedules = execute_query(
        GET_STAFF_SCHEDULE_QUERY, (department_id,), fetch_all=True
    )
    return schedules

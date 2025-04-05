from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ....core.security import get_current_user, check_permissions
from ....utils.db_utils import execute_query
from ....sql.queries.department_queries import *

router = APIRouter()


@router.get("/", response_model=List[dict])
async def get_all_departments(current_user: dict = Depends(get_current_user)):
    """Get all departments"""
    try:
        departments = await execute_query(GET_ALL_DEPARTMENTS_QUERY, fetch_all=True)
        return departments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{dept_id}")
async def get_department(dept_id: int, current_user: dict = Depends(get_current_user)):
    """Get specific department details"""
    department = await execute_query(
        GET_DEPARTMENT_BY_ID_QUERY, (dept_id,), fetch_one=True
    )
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department


@router.post("/")
async def create_department(
    department_data: dict, current_user: dict = Depends(check_permissions(["ADMIN"]))
):
    """Create new department"""
    try:
        result = await execute_query(
            CREATE_DEPARTMENT_QUERY,
            (department_data["name"], department_data["description"]),
            fetch_one=True,
        )
        return {
            "message": "Department created successfully",
            "department_id": result["id"],
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{dept_id}")
async def update_department(
    dept_id: int,
    department_data: dict,
    current_user: dict = Depends(check_permissions(["ADMIN"])),
):
    """Update department details"""
    if not await execute_query(GET_DEPARTMENT_BY_ID_QUERY, (dept_id,), fetch_one=True):
        raise HTTPException(status_code=404, detail="Department not found")

    try:
        await execute_query(
            UPDATE_DEPARTMENT_QUERY,
            (department_data["name"], department_data["description"], dept_id),
        )
        return {"message": "Department updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{dept_id}/staff")
async def get_department_staff(
    dept_id: int, current_user: dict = Depends(get_current_user)
):
    """Get all staff members in a department"""
    staff = await execute_query(GET_DEPARTMENT_STAFF_QUERY, (dept_id,), fetch_all=True)
    return staff

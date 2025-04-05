from fastapi import APIRouter
from .endpoints import (
    auth,
    patient,
    staff,
    finance,
    department,
    appointment,
    admission,
    notification,
)

# Create API router
api_router = APIRouter()

# Include all routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

api_router.include_router(patient.router, prefix="/patients", tags=["Patients"])

api_router.include_router(staff.router, prefix="/staff", tags=["Staff"])

api_router.include_router(finance.router, prefix="/finance", tags=["Finance"])

api_router.include_router(
    department.router, prefix="/departments", tags=["Departments"]
)

api_router.include_router(
    appointment.router, prefix="/appointments", tags=["Appointments"]
)

api_router.include_router(admission.router, prefix="/admissions", tags=["Admissions"])

api_router.include_router(
    notification.router, prefix="/notifications", tags=["Notifications"]
)

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

api_router.include_router(patient.router, prefix="/patient", tags=["Patient"])

api_router.include_router(staff.router, prefix="/staff", tags=["Staff"])

api_router.include_router(finance.router, prefix="/finance", tags=["Finance"])

api_router.include_router(
    department.router, prefix="/department", tags=["Department"]
)

api_router.include_router(
    appointment.router, prefix="/appointment", tags=["Appointment"]
)

api_router.include_router(admission.router, prefix="/admission", tags=["Admission"])

api_router.include_router(
    notification.router, prefix="/notification", tags=["Notification"]
)

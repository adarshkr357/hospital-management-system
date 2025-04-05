from .auth import router as auth_router
from .patient import router as patient_router
from .staff import router as staff_router
from .finance import router as finance_router
from .department import router as department_router
from .appointment import router as appointment_router
from .admission import router as admission_router
from .notification import router as notification_router

__all__ = [
    "auth_router",
    "patient_router",
    "staff_router",
    "finance_router",
    "department_router",
    "appointment_router",
    "admission_router",
    "notification_router",
]

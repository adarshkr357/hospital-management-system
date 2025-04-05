"""
SQL queries package containing all database queries organized by feature.
"""

from .auth_queries import *
from .patient_queries import *
from .staff_queries import *
from .finance_queries import *
from .department_queries import *
from .appointment_queries import *
from .admission_queries import *
from .notification_queries import *

__all__ = [
    "auth_queries",
    "patient_queries",
    "staff_queries",
    "finance_queries",
    "department_queries",
    "appointment_queries",
    "admission_queries",
    "notification_queries",
]

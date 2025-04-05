"""
Database table definitions package.
"""

from .users import CREATE_USERS_TABLE
from .patient import CREATE_PATIENT_TABLES
from .staff import CREATE_STAFF_TABLES
from .finance import CREATE_FINANCE_TABLES
from .notification import CREATE_NOTIFICATION_TABLES

# List of all table creation queries in order of execution
TABLE_CREATION_QUERIES = [
    CREATE_USERS_TABLE,
    CREATE_PATIENT_TABLES,
    CREATE_STAFF_TABLES,
    CREATE_FINANCE_TABLES,
    CREATE_NOTIFICATION_TABLES,
]

__all__ = [
    "CREATE_USERS_TABLE",
    "CREATE_PATIENT_TABLES",
    "CREATE_STAFF_TABLES",
    "CREATE_FINANCE_TABLES",
    "CREATE_NOTIFICATION_TABLES",
    "TABLE_CREATION_QUERIES",
]

import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, List, Dict, Any
from ..config.database import get_db_connection
from ..core.errors import DatabaseError


def execute_query(
    query: str,
    params: tuple = None,
    fetch_all: bool = False,
    fetch_one: bool = False
) -> Optional[Any]:
    """
    Execute a database query with error handling and connection management.
    Returns:
      - If fetch_all is True, a list of dicts.
      - If fetch_one is True, a single dict.
      - Otherwise, returns the status message.
    """
    try:
        with get_db_connection() as connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                
                # If you expect rows back, fetch and commit.
                if fetch_all:
                    result = cursor.fetchall()
                    connection.commit()
                    return [dict(row) for row in result]
                elif fetch_one:
                    result = cursor.fetchone()
                    connection.commit()
                    return dict(result) if result else None
                else:
                    connection.commit()
                    return cursor.statusmessage
    except psycopg2.IntegrityError as e:
        if "unique constraint" in str(e).lower():
            raise DatabaseError("Duplicate entry found")
        elif "foreign key constraint" in str(e).lower():
            raise DatabaseError("Referenced record does not exist")
        else:
            raise DatabaseError(f"Integrity error: {str(e)}")
    except psycopg2.Error as e:
        raise DatabaseError(f"Database error: {str(e)}")
    except Exception as e:
        raise DatabaseError(f"Unexpected error: {str(e)}")

def execute_batch(queries: List[tuple]) -> None:
    """
    Execute multiple queries in a single transaction.
    Each tuple should contain (query, params)
    """
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                for query, params in queries:
                    cursor.execute(query, params)

                connection.commit()
    except Exception as e:
        raise DatabaseError(f"Batch execution failed: {str(e)}")

import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, List, Dict, Any
from ..config.database import get_db_connection
from ..core.errors import DatabaseError


def execute_query(
    query: str, params: tuple = None, fetch_all: bool = False, fetch_one: bool = False
) -> Optional[List[Dict[str, Any]]]:
    """
    Execute database query with error handling and connection management.
    """
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute(query, params)

        if fetch_all:
            result = cursor.fetchall()
            return [dict(row) for row in result]
        elif fetch_one:
            result = cursor.fetchone()
            return dict(result) if result else None
        else:
            connection.commit()
            return cursor.statusmessage

    except psycopg2.IntegrityError as e:
        if connection:
            connection.rollback()
        if "unique constraint" in str(e).lower():
            raise DatabaseError("Duplicate entry found")
        elif "foreign key constraint" in str(e).lower():
            raise DatabaseError("Referenced record does not exist")
        else:
            raise DatabaseError(f"Integrity error: {str(e)}")
    except psycopg2.Error as e:
        if connection:
            connection.rollback()
        raise DatabaseError(f"Database error: {str(e)}")
    except Exception as e:
        if connection:
            connection.rollback()
        raise DatabaseError(f"Unexpected error: {str(e)}")
    finally:
        if connection:
            connection.close()


def execute_batch(queries: List[tuple]) -> None:
    """
    Execute multiple queries in a single transaction.
    Each tuple should contain (query, params)
    """
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        for query, params in queries:
            cursor.execute(query, params)

        connection.commit()
    except Exception as e:
        if connection:
            connection.rollback()
        raise DatabaseError(f"Batch execution failed: {str(e)}")
    finally:
        if connection:
            connection.close()

GET_USER_NOTIFICATIONS_QUERY = """
    SELECT *
    FROM notifications
    WHERE user_id = %s
    ORDER BY created_at DESC;
"""

CREATE_NOTIFICATION_QUERY = """
    INSERT INTO notifications (
        user_id, type, message, created_at
    )
    VALUES (%s, %s, %s, NOW())
    RETURNING id;
"""

MARK_NOTIFICATION_READ_QUERY = """
    UPDATE notifications
    SET read = TRUE
    WHERE id = %s AND user_id = %s
    RETURNING id;
"""


DELETE_NOTIFICATION_QUERY = """
    DELETE FROM notifications
    WHERE id = %s AND user_id = %s
    RETURNING id;
"""

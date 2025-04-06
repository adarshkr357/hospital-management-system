# Authentication related SQL queries
CREATE_USER_QUERY = """
    INSERT INTO users (email, password, role, created_at)
    VALUES (%s, %s, %s, NOW())
    RETURNING id, email, role, created_at;
"""

GET_USER_BY_EMAIL_QUERY = """
    SELECT id, email, password, role, created_at
    FROM users
    WHERE email = %s;
"""

UPDATE_PASSWORD_QUERY = """
    UPDATE users
    SET password = %s
    WHERE email = %s
    RETURNING id;
"""

CREATE_PASSWORD_RESET_TOKEN_QUERY = """
    INSERT INTO password_reset_tokens (user_id, token, expires_at)
    VALUES (%s, %s, NOW() + INTERVAL '1 hour')
    RETURNING token;
"""

VERIFY_RESET_TOKEN_QUERY = """
    SELECT user_id
    FROM password_reset_tokens
    WHERE token = %s AND expires_at > NOW() AND used = FALSE;
"""

INVALIDATE_RESET_TOKEN_QUERY = """
    UPDATE password_reset_tokens
    SET used = TRUE
    WHERE token = %s;
"""

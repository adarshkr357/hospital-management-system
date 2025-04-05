import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
from ..config.settings import Settings

settings = Settings()


async def send_email(
    to_email: str,
    subject: str,
    body_text: str,
    body_html: Optional[str] = None,
    cc: List[str] = None,
    bcc: List[str] = None,
) -> bool:
    """
    Send email using SMTP configuration from settings.
    """
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = settings.SMTP_SENDER
        msg["To"] = to_email

        if cc:
            msg["Cc"] = ", ".join(cc)
        if bcc:
            msg["Bcc"] = ", ".join(bcc)

        # Add text body
        text_part = MIMEText(body_text, "plain")
        msg.attach(text_part)

        # Add HTML body if provided
        if body_html:
            html_part = MIMEText(body_html, "html")
            msg.attach(html_part)

        # Create SMTP connection
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            if settings.SMTP_TLS:
                server.starttls()
            if settings.SMTP_USERNAME and settings.SMTP_PASSWORD:
                server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)

            recipients = [to_email]
            if cc:
                recipients.extend(cc)
            if bcc:
                recipients.extend(bcc)

            server.sendmail(settings.SMTP_SENDER, recipients, msg.as_string())

        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False


async def send_password_reset_email(to_email: str, reset_token: str) -> bool:
    """
    Send password reset email.
    """
    subject = "Password Reset Request"
    reset_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"

    body_text = f"""
    You have requested to reset your password.
    Please click the following link to reset your password:
    {reset_link}
    
    This link will expire in 1 hour.
    If you didn't request this, please ignore this email.
    """

    body_html = f"""
    <html>
        <body>
            <h2>Password Reset Request</h2>
            <p>You have requested to reset your password.</p>
            <p>Please click the following link to reset your password:</p>
            <p><a href="{reset_link}">Reset Password</a></p>
            <p>This link will expire in 1 hour.</p>
            <p>If you didn't request this, please ignore this email.</p>
        </body>
    </html>
    """

    return await send_email(to_email, subject, body_text, body_html)

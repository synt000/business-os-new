import smtplib
from email.message import EmailMessage

from src.core.config import settings


def send_security_alert(subject: str, body: str):

    if not getattr(settings, "SMTP_USERNAME", None):
        return

    if not getattr(settings, "SMTP_PASSWORD", None):
        return

    msg = EmailMessage()

    msg["Subject"] = subject
    msg["From"] = settings.SMTP_USERNAME
    msg["To"] = "sawyannaing054540@gmail.com"

    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(
            settings.SMTP_USERNAME,
            settings.SMTP_PASSWORD
        )
        smtp.send_message(msg)

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from src.core.config import settings


SECURITY_EMAIL = "sawyannaing054540@gmail.com"


def send_security_alert(
    subject: str,
    message: str
):
    """
    Enterprise Security Email Notification Engine
    """

    try:

        smtp_server = getattr(
            settings,
            "SMTP_SERVER",
            "smtp.gmail.com"
        )

        smtp_port = getattr(
            settings,
            "SMTP_PORT",
            587
        )

        smtp_email = getattr(
            settings,
            "SMTP_EMAIL",
            None
        )

        smtp_password = getattr(
            settings,
            "SMTP_PASSWORD",
            None
        )


        if not smtp_email or not smtp_password:
            print(
                "SMTP CONFIG MISSING - SECURITY ALERT LOGGED"
            )
            print(subject)
            print(message)
            return False


        mail = MIMEMultipart()

        mail["From"] = smtp_email
        mail["To"] = SECURITY_EMAIL
        mail["Subject"] = subject


        mail.attach(
            MIMEText(
                message,
                "plain"
            )
        )


        server = smtplib.SMTP(
            smtp_server,
            smtp_port
        )

        server.starttls()

        server.login(
            smtp_email,
            smtp_password
        )


        server.sendmail(
            smtp_email,
            SECURITY_EMAIL,
            mail.as_string()
        )

        server.quit()


        return True


    except Exception as e:

        print(
            "SECURITY EMAIL FAILED:",
            str(e)
        )

        return False



def security_login_alert(
    email,
    ip_address,
    status
):

    return send_security_alert(
        "Business OS Security Login Alert",
        f"""
Business OS Security Event

User:
{email}

Status:
{status}

IP:
{ip_address}
"""
    )



def security_2fa_alert(
    email,
    action
):

    return send_security_alert(
        "Business OS 2FA Security Alert",
        f"""
Two Factor Authentication Event

User:
{email}

Action:
{action}
"""
    )

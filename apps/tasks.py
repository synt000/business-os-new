from .celery import celery_app

@celery_app.task
def send_email_task(to_email, subject, body):
    print(f"Sending email to {to_email}")
    return True

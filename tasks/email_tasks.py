from celery import shared_task
from core.task_store import save_task

@shared_task(bind=True)
def send_email_task(self, to_email, subject, body):
    task_id = self.request.id

    save_task(task_id, {
        "status": "processing",
        "to": to_email
    })

    print("📩 SIMULATED EMAIL:", to_email, subject)

    save_task(task_id, {
        "status": "sent",
        "to": to_email,
        "subject": subject
    })

    return {"status": "sent"}

import time
from celery_app import celery


@celery.task
def add(x: int, y: int) -> int:
    """A fast task — good for seeing immediate results."""
    return x + y


@celery.task(bind=True, max_retries=3)
def send_email(self, to: str, subject: str) -> dict:
    """
    Simulates a slow task (e.g. calling an external email API).

    `bind=True` gives access to `self` (the task instance), which lets
    you inspect metadata and trigger retries.
    """
    try:
        print(f"[send_email] Sending '{subject}' to {to} ...")
        time.sleep(5)  # simulate network latency
        print(f"[send_email] Done.")
        return {"status": "sent", "to": to, "subject": subject}
    except Exception as exc:
        # Retry with exponential back-off: 2s, 4s, 8s
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)

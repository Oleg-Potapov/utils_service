import logging
import smtplib
from email.message import EmailMessage
from celery import Celery
from src.api.config import SMTP_USER, SMTP_PASSWORD, REDIS_HOST, REDIS_PORT, SMTP_HOST, SMTP_PORT

logger = logging.getLogger(__name__)
celery_app = Celery('tasks', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}')


def get_email(to_email: str, subject: str, body: str):
    email = EmailMessage()
    email['Subject'] = subject
    email['From'] = SMTP_USER
    email['To'] = to_email
    email.set_content(body)
    return email


@celery_app.task(bind=True, max_retries=5)
def send_email(self, to_email: str, subject: str, body: str) -> dict:
    try:
        logger.info(f"Start sending email to {to_email} with subject '{subject}'")
        email = get_email(to_email, subject, body)
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(email)
            logger.info(f"Email successfully sent to {to_email}")
            return {"message": "Email is being sent"}
    except Exception as exc:
        logger.error(f"Failed to send email to {to_email}: {exc}", exc_info=True)
        raise self.retry(exc=exc, countdown=60)  # при неудаче повтор через 60 секунд


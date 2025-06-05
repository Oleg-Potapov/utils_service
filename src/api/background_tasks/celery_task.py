import logging
import smtplib
from email.message import EmailMessage
from celery import Celery
from src.api.config import SMTP_USER, SMTP_PASSWORD, REDIS_HOST, REDIS_PORT, SMTP_HOST, SMTP_PORT

logger = logging.getLogger(__name__)
celery_app = Celery('tasks', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}')


def get_email(to_email: str, subject: str, body: str):
    if not body or not body.strip():
        logger.warning(f"Попытка отправить письмо без содержимого на {to_email}, тема: {subject}")
        return None

    signature_text = f"{body}\n\nС уважением, команда OrdenG"
    signature_html = "<br><br><p>С уважением, команда OrdenG</p>"
    full_html = f"""<html><body><p>{body.replace('\\n', '<br>')}</p>{signature_html}</body></html>"""

    email = EmailMessage()
    email['Subject'] = subject
    email['From'] = SMTP_USER
    email['To'] = to_email
    email.set_content(signature_text)
    email.add_alternative(full_html, subtype='html')
    return email


@celery_app.task(bind=True, max_retries=5)
def send_email(self, to_email: str, subject: str, body: str) -> dict:
    try:
        logger.info(f"Start sending email to {to_email} with subject '{subject}'")
        email_ = get_email(to_email, subject, body)
        if email_ is None:  # проверяем, что get_email не вернула None
            logger.warning(f"Не отправляем письмо на {to_email}, тема: {subject}, т.к. body пустой")
            return {"message": "Письмо не отправлено, т.к. body пустой"}
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(email_)
            logger.info(f"Email successfully sent to {email_}")
            return {"message": "Email is being sent"}
    except Exception as exc:
        logger.error(f"Failed to send email to {to_email}: {exc}", exc_info=True)
        raise self.retry(exc=exc, countdown=60)  # при неудаче повтор через 60 секунд


from fastapi import APIRouter
from src.api.background_tasks.celery_task import send_email
from src.api.schemas.email_schemas import EmailSchema, EmailResponse

router = APIRouter(
    tags=["smtp"]
)


@router.post("/send_email", response_model=EmailResponse)
async def smtp_send_email(data: EmailSchema):
    task = send_email.delay(data.email, data.subject, data.body)
    return EmailResponse(task_id=task.id, status="task submitted")


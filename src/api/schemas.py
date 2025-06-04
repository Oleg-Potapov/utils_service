from pydantic import EmailStr, BaseModel


class EmailSchema(BaseModel):
    email: EmailStr
    subject: str
    body: str


class EmailResponse(BaseModel):
    task_id: str
    status: str

    class Config:
        json_schema_extra = {
            "example": {"task_id": "1", "status": "task submitted"}
        }


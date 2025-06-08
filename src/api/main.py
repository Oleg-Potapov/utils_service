import asyncio

import uvicorn
from fastapi import FastAPI
from src.api.routers import send_email_rout, event_cl_httpx, get_rates

app = FastAPI()


app.include_router(event_cl_httpx.router)
app.include_router(get_rates.router)
app.include_router(send_email_rout.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

import logging

from fastapi import FastAPI, status

from src.logger import logger
from src.text.router import router as text_router

app = FastAPI(
    title="ai-voice-bot",
    version="0.0.1",
)


@app.get(
    "/health", summary="Endpoint for health checks", status_code=status.HTTP_200_OK
)
def health_check():
    """
    Endpoint to perform health checks on.
    """
    logger.info("Everything OK!")
    return {"health": "Everything OK!"}


app.include_router(text_router)

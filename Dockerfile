FROM python:3.11-slim

WORKDIR /ai-voice-bot

COPY ./requirements/prod.txt ./requirements.prod

RUN pip install --no-cache-dir -r ./requirements.prod

COPY ./src ./src

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "80"]

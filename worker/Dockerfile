FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY career_worker ./career_worker

CMD ["celery", "-A", "career_worker.celery_app:app", "worker", "--loglevel=INFO"]

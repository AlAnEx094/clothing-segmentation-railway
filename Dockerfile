FROM python:3.9-slim

# 1. Базовые утилиты
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt runtime.txt ./
ENV GIT_TERMINAL_PROMPT=0
RUN pip install --no-cache-dir -r requirements.txt

# 2. Копируем исходники
COPY app ./app

ENV PYTHONUNBUFFERED=1
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

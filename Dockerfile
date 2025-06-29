FROM python:3.9-slim

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- клонируем модель SCHP прямо в контейнер ---
RUN git clone --depth 1 https://github.com/GoGoDuck912/Self-Correction-Human-Parsing.git /opt/schp
ENV PYTHONPATH=/opt/schp:$PYTHONPATH
ENV GIT_TERMINAL_PROMPT=0
# -----------------------------------------------

COPY app ./app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

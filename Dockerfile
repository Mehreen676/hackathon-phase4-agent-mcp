FROM python:3.11-slim

# 1) workdir
WORKDIR /code

# 2) install deps from backend/requirements.txt (IMPORTANT)
COPY backend/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

# 3) copy backend only
COPY backend /code/backend

# 4) run fastapi from backend folder
WORKDIR /code/backend

ENV PORT=7860
EXPOSE 7860

CMD ["gunicorn", "app.main:app", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:7860"]

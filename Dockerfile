FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt



CMD ["gunicorn", "conf.wsgi:application", "--bind", "0.0.0.0:8000"]

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

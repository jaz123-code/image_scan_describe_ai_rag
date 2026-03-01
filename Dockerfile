FROM python:3.12.7

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential

COPY requirements.txt .

RUN mkdir -p /tmp/pip-cache \
    && pip install --upgrade pip \
    && pip install --no-cache-dir --cache-dir=/tmp/pip-cache -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
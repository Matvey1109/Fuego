FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["bash", "-c", "gunicorn main:wsgi_app --bind 0.0.0.0:1111 & uvicorn main:asgi_app --host 0.0.0.0 --port 2222"]

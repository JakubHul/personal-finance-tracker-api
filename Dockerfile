FROM python:3.12-slim

WORKDIR /app

# zależności w osobnej warstwie — cache nie psuje się przy zmianie kodu
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# migracje + start
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]

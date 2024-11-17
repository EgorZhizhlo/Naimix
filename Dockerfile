FROM python:3.11-slim

WORKDIR /app

COPY . .
RUN python -m pip install --upgrade pip&&pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=5000"]
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/
    
EXPOSE 6969

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "6969"]

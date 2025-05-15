FROM python:3.11-alpine

WORKDIR /app

COPY ./docker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY employee_manager/ .

EXPOSE 8003

CMD     ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8003"]
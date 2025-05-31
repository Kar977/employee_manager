# employee_manager

`employee_manager` is a microservice responsible for managing employee-related data in the **BarberShop API** platform. It allows employees to manage their profiles, update schedules, and view upcoming appointments

This service is part of a distributed microservices system and communicates exclusively through the [`gateway_barbershop`](https://github.com/Kar977/gateway_barbershop).

## Features

- Employee profile creation and retrieval  
- Managing personal work schedules  
- Viewing upcoming bookings  
- Uses isolated PostgreSQL database  
- Protected by JWT authentication (validated by the API Gateway)

## Technologies

- Python 3.11  
- FastAPI 0.111.0
- PostgreSQL 15  
- Docker Docker 24.0.7
- Pydantic 2.7  
- Httpx 0.27  
- Pytest  8.3.5 / Pytest-asyncio 0.26.0  
- Pika (RabbitMQ client)  
- Uvicorn 0.30.1

## Environment Variables / Secrets

The following secrets are required (via GitHub Secrets or a local `.env` file):
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_ACCOUNT_ID`
- `POSTGRES_NAME`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`

## ⚙️ Local Development
1. **Clone the repository**
   ```
   git clone https://github.com/Kar977/employee_manager.git
   cd employee_manager
   ```
2. **Build and run using Docker**
   ```
   docker build -t employee_manager .
   docker run --env-file .env -p 8001:8001 customers_manager

   ```
   The service will be available at:
   `http://localhost:8003`

>In production, the service is accessible only through the API Gateway.

### Running Tests
Run all tests using
```
python -m pytest
```

### Deployment
This microservice is containerized and deployed via AWS ECR and Portainer on EC2.

### CI/CD Workflow (GitHub Actions)
1. Lint & Test
Validates code and runs unit/integration tests.

2. Smoke Test
Builds and runs the container to verify basic functionality.

3. Build & Push
Pushes Docker image to AWS ECR.

Final deployment on EC2 is handled manually through Portainer.


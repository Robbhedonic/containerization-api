# Containerization App (Python)

Python microservices project for the Containerization assessment.

Architecture:
- web: Flask (container port 8080, host port 18081)
- api: Flask + PostgreSQL (container port 3000, host port 13001)
- db: PostgreSQL (container port 5432, no host port published)

Synchronous communication:
- web -> api over HTTP
- api -> db over SQL connection

## Requirements

- Docker
- Docker Compose

## Run locally

From the project root:

```bash
docker compose up --build
```

Open in your browser:
- http://localhost:18081

API health endpoint:
- http://localhost:13001/health

Stop services:

```bash
docker compose down
```

## Assessment criteria covered (without AWS)

- Custom app image built with Dockerfile
- Multi-container service (web + api + db)
- Synchronous communication between containers
- Reproducible local execution with Docker Compose

## Docker Hub (push images)

1. Sign in:

```bash
docker login
```

2. Build images:

```bash
docker compose build
```

3. Tag images (replace TU_USUARIO):

```bash
docker tag todo-web TU_USUARIO/todo-web:1.0.0
docker tag todo-api TU_USUARIO/todo-api:1.0.0
```

4. Push:

```bash
docker push TU_USUARIO/todo-web:1.0.0
docker push TU_USUARIO/todo-api:1.0.0
```

## Short screencast script

1. Explain the architecture (web, api, db).
2. Show the web and api Dockerfiles.
3. Start everything with docker compose up --build.
4. Demo create, toggle, and delete todo actions.
5. Show service-to-service communication with logs.
6. Show image tags and Docker Hub push commands.

## Deploy to AWS EC2 (now)

This project can be deployed on one EC2 instance using Docker Compose.

### 1. Push your images to Docker Hub

From your local machine:

```bash
docker login
docker compose build
docker tag containerization-app-web YOUR_DOCKERHUB_USER/todo-web:1.0.0
docker tag containerization-app-api YOUR_DOCKERHUB_USER/todo-api:1.0.0
docker push YOUR_DOCKERHUB_USER/todo-web:1.0.0
docker push YOUR_DOCKERHUB_USER/todo-api:1.0.0
```

### 2. Create EC2 instance

- AMI: Ubuntu 24.04 LTS
- Instance type: t2.micro (or t3.micro)
- Security Group inbound rules:
	- SSH (22) from your IP
	- HTTP (80) from Anywhere

### 3. Install Docker + Compose on EC2

SSH into EC2 and run:

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-v2
sudo usermod -aG docker $USER
newgrp docker
docker --version
docker compose version
```

### 4. Copy deployment files to EC2

From your local machine (replace path, key, and host):

```bash
scp -i /path/to/key.pem deploy/aws-ec2/docker-compose.ec2.yml ubuntu@EC2_PUBLIC_IP:~/docker-compose.yml
scp -i /path/to/key.pem deploy/aws-ec2/.env.ec2.example ubuntu@EC2_PUBLIC_IP:~/.env
scp -i /path/to/key.pem deploy/aws-ec2/init.sql ubuntu@EC2_PUBLIC_IP:~/init.sql
```

Then on EC2, edit .env and set your values:

```bash
nano ~/.env
```

Set:
- DOCKERHUB_USER
- IMAGE_TAG
- DB_USER
- DB_PASSWORD

### 5. Start services on EC2

On EC2:

```bash
docker compose --env-file .env up -d
docker compose ps
docker compose logs -f web
```

### 6. Validate deployment

- Open http://EC2_PUBLIC_IP
- You should see the Todo web app
- API is private inside Docker network (recommended)

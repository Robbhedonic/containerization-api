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

# Containerization App (Python)

Proyecto de microservicios en Python para la evaluación de Containerization.

Arquitectura:
- web: Flask (contenedor 8080, host 18081)
- api: Flask + PostgreSQL (contenedor 3000, host 13001)
- db: PostgreSQL (contenedor 5432, sin puerto publicado en host)

Comunicación síncrona:
- web -> api por HTTP
- api -> db por conexión SQL

## Requisitos

- Docker
- Docker Compose

## Ejecutar local

Desde la raíz del proyecto:

```bash
docker compose up --build
```

Abrir en navegador:
- http://localhost:18081

Health API:
- http://localhost:13001/health

Parar servicios:

```bash
docker compose down
```

## Criterios de evaluación cubiertos (sin AWS)

- Imagen propia de la app con Dockerfile
- Servicio con múltiples contenedores (web + api + db)
- Comunicación síncrona entre contenedores
- Ejecución reproducible con Docker Compose

## Docker Hub (push de imágenes)

1. Iniciar sesión:

```bash
docker login
```

2. Construir imágenes:

```bash
docker compose build
```

3. Etiquetar imágenes (cambia TU_USUARIO):

```bash
docker tag todo-web TU_USUARIO/todo-web:1.0.0
docker tag todo-api TU_USUARIO/todo-api:1.0.0
```

4. Publicar:

```bash
docker push TU_USUARIO/todo-web:1.0.0
docker push TU_USUARIO/todo-api:1.0.0
```

## Guion corto para screencast

1. Explicar la arquitectura (web, api, db).
2. Mostrar Dockerfile de web y api.
3. Levantar con docker compose up --build.
4. Probar creación, toggle y eliminación de tareas.
5. Mostrar comunicación entre servicios con logs.
6. Enseñar etiquetas y comandos de push a Docker Hub.

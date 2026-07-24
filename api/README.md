# API de Inventario y Benchmarks de Hardware

## Descripción

Proyecto desarrollado para el curso de Sistemas Operativos.

La aplicación implementa una API REST utilizando Flask y PostgreSQL, desplegada mediante Docker Compose. Permite registrar componentes de hardware y realizar pruebas de carga para observar el consumo de recursos del contenedor.

## Tecnologías

- Ubuntu Server 24.04 LTS
- Python 3.12
- Flask
- PostgreSQL 16
- Docker
- Docker Compose

## Levantar el proyecto

```bash
docker compose up -d --build
```

## Detener el proyecto

```bash
docker compose down
```

## Endpoints principales

- GET /
- GET /health
- GET /api/component-types
- POST /api/component-types
- GET /api/components
- POST /api/components
- PUT /api/components/{id}
- DELETE /api/components/{id}
- GET /api/benchmarks/cpu

## Prueba de estrés

```bash
curl "http://localhost:8080/api/benchmarks/cpu?iterations=1500000"
```

## Monitoreo

```bash
docker stats
```

## Persistencia

La base de datos utiliza un volumen Docker (`postgres_data`) para conservar la información incluso después de reiniciar los contenedores.

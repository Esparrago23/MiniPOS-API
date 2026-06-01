# MiniPOS API

API REST para la app Flutter de punto de venta.

## Requisitos

- Python 3.13 o superior

## Instalacion

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Ejecutar

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Si vas a probar desde un celular fisico en la misma red:

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints iniciales

```text
GET  /health
POST /auth/register
POST /auth/login
GET  /auth/me

GET    /products
POST   /products
GET    /products/{id}
GET    /products/barcode/{barcode}
PUT    /products/{id}
DELETE /products/{id}

GET  /sales
POST /sales
GET  /sales/{id}
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

## Body de registro

```json
{
  "name": "Ana Lopez",
  "email": "ana@example.com",
  "password": "123456"
}
```

## Body de login

```json
{
  "email": "ana@example.com",
  "password": "123456"
}
```

La base de datos SQLite se crea automaticamente como `minipos.db` al iniciar la API.

## Autenticacion

Los endpoints de productos y ventas requieren token:

```http
Authorization: Bearer TU_TOKEN
```

El token se obtiene desde `/auth/register` o `/auth/login`.

## Docker

Construir y ejecutar:

```powershell
docker compose up -d --build
```

Ver logs:

```powershell
docker compose logs -f api
```

Detener:

```powershell
docker compose down
```

La base de datos dentro de Docker se guarda en un volumen llamado `minipos_data`.

## Deploy

Para EC2 revisa:

```text
EC2_DEPLOY.md
```

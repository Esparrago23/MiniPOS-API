# MiniPOS API

API REST para MiniPOS, una aplicacion de inventario y punto de venta hecha con Flutter. Permite registrar usuarios, autenticar sesiones, administrar productos y guardar ventas con descuento automatico de stock.

## Funcionalidades

- Registro e inicio de sesion con token tipo JWT.
- CRUD de productos.
- Busqueda de productos por codigo de barras.
- Registro y consulta de ventas.
- Base de datos SQLite para ejecucion local o demo.
- Ejecucion local con Python o contenedores Docker.

## Tecnologias

- Python 3.13.
- FastAPI.
- SQLAlchemy.
- SQLite.
- Docker y Docker Compose.

## App Flutter

Esta API fue desarrollada para la app MiniPOS.

Repositorio de la app:

```text
https://github.com/Esparrago23/MiniPOS
```

## Configuracion

Antes de ejecutar la API, crea un archivo `.env` desde el ejemplo:

```powershell
Copy-Item .env.example .env
```

Edita `.env` y cambia `SECRET_KEY` por un valor privado de al menos 32 caracteres. No subas `.env` a GitHub.

Variables disponibles:

```env
SECRET_KEY=change-this-to-a-long-random-secret-before-running
ACCESS_TOKEN_EXPIRE_MINUTES=480
DATABASE_URL=sqlite:///./data/minipos.db
ALLOWED_ORIGINS=*
```

## Ejecutar con Docker

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

La base de datos queda guardada en el volumen `minipos_data`.

## Ejecutar localmente

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Si vas a probar desde un celular fisico en la misma red, ejecuta la API con:

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Documentacion interactiva

Con la API ejecutandose:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
GET http://127.0.0.1:8000/health
```

## Endpoints principales

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

Los endpoints de productos y ventas requieren:

```http
Authorization: Bearer TU_TOKEN
```

## Conectar con la app Flutter

La app no trae URL hardcodeada. Al ejecutarla o compilarla debes pasar la URL de esta API:

```powershell
flutter run --dart-define=API_BASE_URL=http://127.0.0.1:8000
```

Para Android Emulator usa:

```powershell
flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8000
```

Para celular fisico usa la IP de la computadora o del servidor:

```powershell
flutter run --dart-define=API_BASE_URL=http://IP_DEL_SERVIDOR:8000
```

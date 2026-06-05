# MiniPOS API Contract

Este contrato sirve para conectar la app Flutter con la API FastAPI.

## Base URL

Para Flutter Web o pruebas desde la misma PC:

```text
http://127.0.0.1:8000
```

Para Android Emulator:

```text
http://10.0.2.2:8000
```

Para celular fisico:

```text
http://IP_DE_TU_PC:8000
```

En celular fisico la API debe ejecutarse con:

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Health

```http
GET /health
```

Respuesta:

```json
{
  "status": "ok"
}
```

## Register

```http
POST /auth/register
Content-Type: application/json
```

Request:

```json
{
  "name": "Ana Lopez",
  "email": "ana@example.com",
  "password": "123456"
}
```

Response 201:

```json
{
  "token": "jwt-like-token",
  "user": {
    "id": 1,
    "name": "Ana Lopez",
    "email": "ana@example.com"
  }
}
```

Errores principales:

```text
400 Email already registered.
422 Validation error.
```

## Login

```http
POST /auth/login
Content-Type: application/json
```

Request:

```json
{
  "email": "ana@example.com",
  "password": "123456"
}
```

Response 200:

```json
{
  "token": "jwt-like-token",
  "user": {
    "id": 1,
    "name": "Ana Lopez",
    "email": "ana@example.com"
  }
}
```

Errores principales:

```text
401 Invalid email or password.
422 Validation error.
```

## Auth Me

```http
GET /auth/me
Authorization: Bearer TOKEN
```

Response 200:

```json
{
  "id": 1,
  "name": "Ana Lopez",
  "email": "ana@example.com"
}
```

## Products

Todos los endpoints de productos requieren:

```http
Authorization: Bearer TOKEN
```

### Listar productos

```http
GET /products
```

Response 200:

```json
[
  {
    "id": 1,
    "name": "Refresco Cola 600ml",
    "barcode": "7501234567890",
    "price": 18.5,
    "stock": 10,
    "category": "Bebidas",
    "created_at": "2026-05-31T19:15:35",
    "updated_at": "2026-05-31T19:15:35"
  }
]
```

### Crear producto

```http
POST /products
Content-Type: application/json
Authorization: Bearer TOKEN
```

Request:

```json
{
  "name": "Refresco Cola 600ml",
  "barcode": "7501234567890",
  "price": 18.5,
  "stock": 10,
  "category": "Bebidas"
}
```

### Obtener producto por id

```http
GET /products/1
Authorization: Bearer TOKEN
```

### Obtener producto por codigo de barras

Este endpoint es el que debe usar el scanner de la app Flutter.

```http
GET /products/barcode/7501234567890
Authorization: Bearer TOKEN
```

### Actualizar producto

```http
PUT /products/1
Content-Type: application/json
Authorization: Bearer TOKEN
```

Request:

```json
{
  "name": "Refresco Cola 600ml",
  "barcode": "7501234567890",
  "price": 19.0,
  "stock": 12,
  "category": "Bebidas"
}
```

Tambien puedes mandar solo los campos que cambian.

### Eliminar producto

```http
DELETE /products/1
Authorization: Bearer TOKEN
```

Response 200:

```json
{
  "message": "Product deleted."
}
```

## Sales

Todos los endpoints de ventas requieren:

```http
Authorization: Bearer TOKEN
```

### Crear venta

```http
POST /sales
Content-Type: application/json
Authorization: Bearer TOKEN
```

Request:

```json
{
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    }
  ]
}
```

Response 201:

```json
{
  "id": 1,
  "user_id": 1,
  "total": 37.0,
  "created_at": "2026-05-31T19:15:35",
  "items": [
    {
      "id": 1,
      "product_id": 1,
      "product_name": "Refresco Cola 600ml",
      "barcode": "7501234567890",
      "quantity": 2,
      "unit_price": 18.5,
      "subtotal": 37.0
    }
  ]
}
```

La API descuenta stock automaticamente al crear la venta.

### Listar ventas

```http
GET /sales
Authorization: Bearer TOKEN
```

### Obtener venta por id

```http
GET /sales/1
Authorization: Bearer TOKEN
```

## Conexion desde Flutter

La app MiniPOS recibe la URL de la API por `--dart-define`:

```powershell
flutter run --dart-define=API_BASE_URL=http://127.0.0.1:8000
```

Usa `http://10.0.2.2:8000` para Android Emulator y `http://IP_DEL_SERVIDOR:8000` para celular fisico o servidor remoto.

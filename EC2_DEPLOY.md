# Deploy en AWS EC2 con Docker

Guia rapida para subir MiniPOS API a una instancia EC2.

## 1. Preparar EC2

Usa Ubuntu Server. Abre estos puertos en el Security Group:

```text
22   SSH
8000 API
```

Para pruebas escolares basta con el puerto 8000. En produccion real se usaria HTTPS con Nginx o un load balancer.

## 2. Instalar Docker

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-plugin
sudo usermod -aG docker ubuntu
newgrp docker
```

## 3. Subir el proyecto

Desde tu PC puedes comprimir la carpeta `minipos` o subirla con Git. En la instancia debe quedar una carpeta con:

```text
app/
Dockerfile
docker-compose.yml
requirements.txt
.env
```

## 4. Crear `.env`

En EC2:

```bash
cp .env.example .env
nano .env
```

Cambia `SECRET_KEY` por un texto largo y privado.

## 5. Levantar la API

```bash
docker compose up -d --build
```

Ver logs:

```bash
docker compose logs -f api
```

Probar:

```bash
curl http://PUBLIC_IP_EC2:8000/health
```

Swagger:

```text
http://PUBLIC_IP_EC2:8000/docs
```

## 6. URL para Flutter

Cuando la API este en EC2, la app Flutter debe usar:

```text
http://PUBLIC_IP_EC2:8000
```

No uses `127.0.0.1` desde celular, porque eso apunta al propio celular.

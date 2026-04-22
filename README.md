# sistema-encomiendas-django

Proyecto base del Sistema de Gestion de Encomiendas desarrollado con Django, PostgreSQL y Docker.

## Estructura

- `config`: configuracion global del proyecto Django.
- `envios`, `clientes`, `rutas`: apps base del dominio.
- `Dockerfile` y `docker-compose.yml`: entorno de desarrollo con Django + PostgreSQL.

## Puesta en marcha

1. Crear `.env` a partir de `.env.example`.
2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecutar localmente:

```bash
python manage.py runserver
```

4. Ejecutar con Docker:

```bash
docker compose up --build
```

## Comandos utiles

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
docker compose exec web python manage.py migrate
```

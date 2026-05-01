# Encomiendas

Sistema de Gestión de Encomiendas desarrollado con Django, PostgreSQL y Docker.

## Estructura del proyecto

```text
encomiendas/
├── config/
│   ├── settings.py
│   └── urls.py
├── envios/
│   ├── views.py
│   ├── views_auth.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── templates/
│   ├── base.html
│   ├── navbar.html
│   ├── index.html/
│   │   ├── dashboard.html
│   │   ├── lista.html
│   │   ├── detalle.html
│   │   └── form.html
│   └── accounts/
│       ├── login.html
│       └── register.html
├── static/
│   ├── css/styles.css
│   └── js/main.js
├── Dockerfile
├── docker-compose.yml
└── .env
```

## Requisitos

- Python 3.11+
- Docker y Docker Compose

## Configuración inicial

1. Crear archivo de entorno:

```bash
cp .env.example .env
```

2. Ajustar variables en `.env` (DB, credenciales y host permitidos).

## Ejecutar con Docker (recomendado)

```bash
docker compose up --build
```

Servicios:

- App Django (Gunicorn + Nginx): `http://localhost`
- PostgreSQL: `localhost:5432`
- pgAdmin: `http://localhost:5050`

## Migraciones y superusuario

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

## Ejecutar en local (sin Docker)

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Pruebas

```bash
python manage.py test
```

## Flujo funcional implementado

- Login, logout y perfil.
- Dashboard de encomiendas.
- Lista de encomiendas con filtros.
- Detalle de encomienda con historial de estados.
- Registro de nueva encomienda.
- Admin de Django configurado con badges y fieldsets.

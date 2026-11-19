# Sistema de Gestión de Préstamos UNCP

Proyecto Django desarrollado para el Caso 1 de la práctica de Desarrollo de Aplicaciones Web.

## Instalación

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_practica
python manage.py runserver
```

## Datos de prueba

- Administrador: `admin` / `Admin123!`
- Docentes: `docente1` a `docente5` / `Docente123!`
- Asistentes: `asistente1` y `asistente2` / `Asistente123!`

Accesos:

- Catálogo público: `/`
- Iniciar sesión: `/login/`
- Django Admin: `/admin/`

## Funcionalidades

Incluye modelos de laboratorios, equipos y préstamos; perfiles por rol; formularios con validaciones, sanitización con Bleach, Django Admin personalizado, middleware de auditoría y alertas de vencidos, timeout de sesión de 30 minutos y permisos por rol.

## Entrega

El documento PDF con carátula y evidencias se genera con:

```bash
python generar_entrega.py
```

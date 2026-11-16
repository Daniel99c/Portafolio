# Backend del portafolio (Django)

Administra el contenido del portafolio, recibe los mensajes de contacto y guarda estadísticas anónimas.

## Puesta en marcha

```bash
cd backend
..\venv\Scripts\activate
pip install -r ..\requirements.txt
copy .env.example .env      # y completa los valores
python manage.py migrate
python manage.py createsuperuser
python manage.py cargar_contenido   # solo la primera vez
python manage.py runserver
```

El panel de administración está en la dirección `ADMIN_URL` del `.env`, no en `/admin/`.

## Qué se administra

| Sección del admin | Para qué sirve |
| --- | --- |
| Contenido del portafolio | Perfil, hoja de vida, ficha, stack, experiencia, proyectos y certificados |
| Contacto → Mensajes | Mensajes del formulario (también llegan al correo) |
| Estadísticas | Visitas, secciones vistas, descargas de la hoja de vida, certificados y repositorios |

Un certificado con **Mostrar documento** desmarcado aparece en la lista, pero su PDF nunca se entrega.

## API

| Método | Ruta | Descripción |
| --- | --- | --- |
| GET | `/api/portfolio/` | Todo el contenido público |
| GET | `/api/cv/` | Hoja de vida (`?download=1` para descargar) |
| GET | `/api/certificates/<id>/file/` | PDF de un certificado público |
| POST | `/api/contact/` | Formulario de contacto (requiere token de Turnstile) |
| POST | `/api/events/` | Estadísticas: `visit`, `page`, `repo` |

## Seguridad incluida

- Datos privados en `.env` (fuera de git).
- Admin en una ruta secreta y bloqueo tras 5 intentos fallidos (django-axes). Desbloquear: `python manage.py axes_reset`.
- CORS solo para las direcciones de `CORS_ALLOWED_ORIGINS`.
- Límite de peticiones por IP: 5 mensajes por hora y 600 consultas por hora.
- Formulario protegido con Cloudflare Turnstile, un campo trampa y correo en texto plano (sin HTML).
- Archivos privados en `private_media/`, que nunca se publican directamente.
- Con `DEBUG=False`: HTTPS obligatorio, HSTS, cookies seguras y protección contra clickjacking.

## Antes de publicar

1. En `.env`: `DEBUG=False`, una `SECRET_KEY` nueva, tu dominio en `ALLOWED_HOSTS` y `CORS_ALLOWED_ORIGINS`.
2. Crea un sitio en Cloudflare Turnstile y coloca la llave secreta en `TURNSTILE_SECRET_KEY` (backend) y la llave pública en `VITE_TURNSTILE_SITE_KEY` (frontend).
3. `python manage.py check --deploy` debe pasar sin errores.
4. `python manage.py collectstatic` y configura el servidor web para servir `/static/` y `/media/`.

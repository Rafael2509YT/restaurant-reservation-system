# Restaurant Reservation System 🍽️

Sistema de gestión de reservaciones para restaurantes, desarrollado con **Django + DRF** en el backend y **Vue 3 (Composition API) + Pinia** en el frontend.

## 🚀 Cómo correr localmente

### 1. Backend (Django)
*   Navega a la carpeta: `cd backend`
*   Crea un entorno virtual: `python -m venv venv`
*   Activa el entorno: 
    *   Windows: `.\venv\Scripts\activate`
    *   Linux/Mac: `source venv/bin/activate`
*   Instala dependencias: `pip install -r requirements.txt`
*   Ejecuta migraciones: `python manage.py migrate`
*   Inicia el servidor: `python manage.py runserver`
    *   *El backend correrá en `http://localhost:8000`*

### 2. Frontend (Vue 3)
*   Navega a la carpeta: `cd frontend/y`
*   Instala dependencias: `npm install`
*   Inicia el servidor de desarrollo: `npm run dev`
    *   *El frontend correrá en `http://localhost:5173`*

---

## 🔐 Variables de Entorno

### Backend (`/backend/.env`)
| Variable | Descripción | Ejemplo |
| :--- | :--- | :--- |
| `SECRET_KEY` | Clave secreta de Django | `django-insecure-dwg$i=@&%2^a&@f#5deybd=jv!8mg#$(!&xslze+w=k$p5w$-b` |
| `DEBUG` | Modo Depuración | `True` o `False` |
| `DATABASE_URL` | URL de conexión PostgreSQL Externa render| `postgresql://restaurant_db_0lul_user:j9vbKAbdHJsVpC5V2ufVfrLpiYk6KnMm@dpg-d6o7pop5pdvs73ec26i0-a.oregon-postgres.render.com/restaurant_db_0lul` |
| `ALLOWED_HOSTS` | Hosts permitidos | `localhost,127.0.0.1,.onrender.com` |

### Frontend (`/frontend/y/.env.local`)
| Variable | Descripción | Ejemplo |
| :--- | :--- | :--- |
| `VITE_API_URL` | URL base del backend | `http://localhost:8000/api` |

---

## 🌍 Cómo desplegar

### Backend & DB (**Render**)
1.  Crea un servicio de **PostgreSQL** en Render.
2.  Crea un **Web Service**, conecta tu repo de GitHub.
3.  Configura las variables de entorno mencionadas arriba.
4.  Comando de Build: `./build.sh` (o `pip install -r requirements.txt`).
5.  Comando de Start: `gunicorn config.wsgi:application`.

### Frontend (**Vercel**)
1.  Conecta tu repo a Vercel.
2.  Configura el *Root Directory* como `frontend/y`.
3.  Añade la variable `VITE_API_URL` apuntando a tu URL de Render.
4.  Vercel detectará automáticamente que es un proyecto **Vite**.

---

## 🔗 URLs de Producción
*   **Frontend**: [https://restaurant-reservation-system-self.vercel.app](https://restaurant-reservation-system-self.vercel.app)
*   **Backend API**: [https://restaurant-backend-7mem.onrender.com](https://restaurant-backend-7mem.onrender.com)

---

## 🛠️ Herramientas de Utilidad

### Vaciar Base de Datos (Mesas y Reservas)
He incluido un comando personalizado para limpiar las tablas y reiniciar los contadores de ID de forma segura:

```powershell
# Desde la carpeta /backend
python manage.py clear_data
```
*Este comando pedirá confirmación antes de proceder. También puedes usar `--no-confirm` para ejecución directa en scripts.*

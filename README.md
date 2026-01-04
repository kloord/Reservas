# Sistema de Reservas de Cabañas (Flask + React + Vite)

Aplicación web de administración de reservas para un complejo de 16 cabañas, construida con Flask (backend) y React + Vite (frontend). En esta fase inicial, toda la información se gestiona en memoria para pruebas y validación de la lógica de negocio; la arquitectura está preparada para integrar una base de datos posteriormente.

## Arquitectura

- Backend (`backend/`): API REST en Flask con:
  - Modelos en memoria: `Cabin` y `Reservation`.
  - Servicios: `CabinService` y `ReservationService` (CRUD y reglas de negocio).
  - Endpoints: cabañas, reservas y disponibilidad.
  - CORS configurado para el frontend.
- Frontend (`frontend/`): Panel de administración en React + Vite con:
  - Selector de rango de fechas.
  - Grid de cabañas con estado (disponible/ocupada) según fechas.
  - Modal para crear/editar/eliminar reservas.
  - Servicios `axios` para consumir la API.

## Ejecutar localmente

Requisitos: Python 3.10+, Node.js 18+, npm.

1. Backend
   ```zsh
   cd backend
   python3 -m venv .venv
   . .venv/bin/activate
   pip install -r requirements.txt
   # Puertos: usa 5001 para evitar conflictos locales
   PORT=5001 python run.py
   # Salud: http://localhost:5001/health
   ```

2. Frontend
   ```zsh
   cd frontend
   npm install
   npm run dev
   # App: http://localhost:5173/
   ```

El `vite.config.js` tiene proxy a `http://localhost:5001/api`.

### Simulación de reservas (seed)

Con el backend corriendo, puedes poblar datos de prueba:

```zsh
cd backend
pip install -r requirements.txt  # asegura 'requests'
python scripts/seed_reservations.py --count 12 --base-url http://localhost:5001
```

Opciones útiles:
- `--count N`: cantidad de reservas a crear (por defecto 12).
- `--start-offset DAYS`: mínimo de días desde hoy para comenzar (por defecto 2).
- `--window DAYS`: ventana de días a futuro para distribuir (por defecto 30).
- `--dry-run`: no crea reservas; solo muestra lo que generaría.

Reglas respetadas por el seed:
- Cabañas 21–24 (Express) máximo 4 días de estadía.
- Resto de cabañas entre 2 y 7 días.

## Despliegue paso a paso (Vercel + Render + Cloudflare Access)

### 1) Preparar el proyecto
- Frontend: usa `VITE_API_BASE` para apuntar al backend en producción.
  - Archivo ejemplo: `frontend/.env.example`.
- Backend: listo para WSGI con `gunicorn` usando `backend/wsgi.py`.

### 2) Backend en Render (o Railway)
1. Crear un nuevo servicio web desde el directorio `backend/` del repositorio.
2. Variables de entorno:
  - `PORT`: Render lo define automáticamente (no fijar manualmente).
  - `MONGODB_URI`: cuando migres a Atlas.
3. Comando de inicio:
  ```
  gunicorn -b 0.0.0.0:$PORT wsgi:app
  ```
4. Health check opcional: `/health`.

### 3) Frontend en Vercel
1. Importar el repositorio y seleccionar el directorio `frontend/`.
2. Variables de entorno:
  - `VITE_API_BASE`: URL pública del backend, por ejemplo `https://tu-backend.onrender.com/api`.
3. Comandos:
  - Build: `npm run build`
  - Output: `dist`

### 4) Acceso sólo para administradores y supervisores
- Configurar Cloudflare Access (Zero Trust → Applications) sobre los dominios del frontend y/o backend.
- Políticas: permitir sólo correos/dominios de tu equipo.
- Resultado: puerta de acceso gestionada sin modificar el código de la app.

### 5) CORS y seguridad
- En `backend/app/__init__.py`, CORS está habilitado; añade tu dominio de Vercel en `origins` si lo necesitas.
- Guarda secretos (URIs, tokens) como variables de entorno en Render/Vercel.

### 6) Observabilidad y backups
- Atlas: clúster replicado, backups automáticos y opcional PITR.
- Render/Vercel: logs y alertas básicas desde sus paneles.

Con esto tienes un flujo simple, disponible y con integridad (cuando migres a Atlas con índices y transacciones). 

## API (resumen)

- `GET /api/cabins` — Lista todas las cabañas.
- `GET /api/cabins/:id` — Obtiene una cabaña.
- `PUT /api/cabins/:id` — Actualiza una cabaña.
- `GET /api/reservations` — Lista reservas; filtros `cabin_id`, `start_date`, `end_date`.
- `GET /api/reservations/:id` — Obtiene una reserva.
- `POST /api/reservations` — Crea reserva: `{ cabin_id, guest_name, start_date, end_date, num_guests, guest_email?, guest_phone?, notes? }`.
- `PUT /api/reservations/:id` — Actualiza reserva.
- `DELETE /api/reservations/:id` — Elimina reserva.
- `GET /api/availability?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD` — Disponibilidad detallada.
- `GET /api/availability/summary?...` — Resumen de disponibilidad.

## Lógica de reservas y validación

- Rango de fechas: `$start < end$` obligatorio; se valida formato ISO.
- Sin solapamientos por cabaña: dos reservas se solapan si `$start_a < end_b \land end_a > start_b$`.
- Capacidad: `num_guests <= cabin.capacity`.
- En esta fase, no se permiten reservas con fecha de inicio en el pasado.
- Servicios devuelven tuplas `(resultado, error)` y los endpoints normalizan respuestas JSON.

## Migración futura a Base de Datos

- Sustituir servicios en memoria por repositorios (p. ej., SQLAlchemy) manteniendo la misma interfaz pública:
  - `CabinService`: `get_all`, `get_by_id`, `update` → tablas `cabins`.
  - `ReservationService`: `create`, `update`, `delete`, `get_by_*`, `check_availability` → tablas `reservations` con índice en `(cabin_id, start_date, end_date)`.
- Mantener la lógica de solapamiento a nivel de dominio y, opcionalmente, reforzar con constraints/validaciones en transacciones.
- Añadir configuración (`config.py`), sesiones de DB y blueprints sin cambiar rutas ni contratos.

## Calidad y extensibilidad

- Código modular y claro, preparado para escalar.
- UI simple y profesional: estado por fechas dinámico, flujos de CRUD administrativos.
- CORS y proxy listos para desarrollo local.

## Notas

- Modelo de datos en memoria para pruebas; no persistente.
- Al pasar a producción, usar WSGI (Gunicorn) y una base de datos (PostgreSQL/MySQL) con migraciones.

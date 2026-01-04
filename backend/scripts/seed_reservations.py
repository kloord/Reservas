#!/usr/bin/env python3
"""
Script de simulación de reservas para pruebas.

Este script genera reservas de prueba y las crea en el backend vía HTTP
usando los endpoints REST. Útil para poblar el calendario y verificar la lógica.

Requisitos:
- Backend ejecutándose (por defecto: http://localhost:5001)
- `pip install -r backend/requirements.txt` (usa `requests`)

Uso:
    python scripts/seed_reservations.py --count 12 --base-url http://localhost:5001
Opciones:
    --count N                Número de reservas a intentar crear (por defecto 12)
    --base-url URL           Base URL del backend (por defecto http://localhost:5001)
    --start-offset DAYS      Offset mínimo en días desde hoy para la fecha de inicio (por defecto 2)
    --window DAYS            Ventana en días a futuro donde generar fechas (por defecto 30)
    --dry-run                No envía al backend; solo muestra las reservas generadas
"""
import argparse
import random
from datetime import date, timedelta
import requests

def fetch_cabins(base_url: str):
    r = requests.get(f"{base_url}/api/cabins")
    r.raise_for_status()
    return r.json()["data"]

def post_reservation(base_url: str, payload: dict):
    r = requests.post(f"{base_url}/api/reservations", json=payload)
    try:
        r.raise_for_status()
    except requests.HTTPError:
        # Devuelve error legible del backend si existe
        try:
            data = r.json()
            msg = data.get("message") or data.get("error") or r.text
        except Exception:
            msg = r.text
        raise RuntimeError(f"Error creando reserva: {msg}")
    return r.json()["data"]

def random_guest(n: int):
    names = [
        "Ana", "Luis", "María", "José", "Carla",
        "Pedro", "Lucía", "Diego", "Sofía", "Jorge"
    ]
    surnames = ["González", "Pérez", "Rodríguez", "Suárez", "López", "Gómez"]
    name = f"{random.choice(names)} {random.choice(surnames)}"
    return {
        "guest_name": name,
        "guest_email": f"{name.split()[0].lower()}{n}@example.com",
        "guest_phone": f"+56 9 555{n:04d}"
    }

def gen_reservation_for_cabin(cabin: dict, start_day: date):
    # Duración: 1-4 días para Express (21–24), 2-7 para el resto
    if cabin["id"] in {21, 22, 23, 24}:
        duration = random.randint(1, 4)
    else:
        duration = random.randint(2, 7)
    end_day = start_day + timedelta(days=duration)

    g = random_guest(random.randint(1, 9999))
    payload = {
        "cabin_id": cabin["id"],
        "guest_name": g["guest_name"],
        "guest_email": g["guest_email"],
        "guest_phone": g["guest_phone"],
        "start_date": start_day.isoformat(),
        "end_date": end_day.isoformat(),
        "num_guests": random.randint(1, min(6, cabin.get("capacity", 4))),
        "notes": "Simulación de reserva"
    }
    return payload

def main():
    ap = argparse.ArgumentParser(description="Genera reservas de simulación contra la API")
    ap.add_argument("--count", type=int, default=12)
    ap.add_argument("--base-url", type=str, default="http://localhost:5001")
    ap.add_argument("--start-offset", type=int, default=2)
    ap.add_argument("--window", type=int, default=30)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    cabins = fetch_cabins(args.base_url)
    if not cabins:
        print("No hay cabañas disponibles desde la API")
        return

    # Generar fechas aleatorias dentro de la ventana a futuro
    today = date.today()
    created = 0
    attempts = 0
    errors = 0
    max_attempts = args.count * 3

    print(f"Intentando crear {args.count} reservas de simulación...")
    while created < args.count and attempts < max_attempts:
        attempts += 1
        cabin = random.choice(cabins)
        offset = random.randint(args.start_offset, args.window)
        start_day = today + timedelta(days=offset)
        payload = gen_reservation_for_cabin(cabin, start_day)

        if args.dry_run:
            print(f"[DRY] {payload}")
            created += 1
            continue

        try:
            res = post_reservation(args.base_url, payload)
            created += 1
            print(f"✓ Reserva creada: {res['id']} | Cabaña {res['cabin_id']} | {res['guest_name']} | {res['start_date']} → {res['end_date']}")
        except Exception as e:
            errors += 1
            print(f"✗ {e}")

    print(f"Listo. Creadas: {created}, errores: {errors}, intentos: {attempts}")

if __name__ == "__main__":
    main()

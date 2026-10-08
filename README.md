# Gym Website (Django)

Built on the "Gymnast" template by HTML Codex. **Keep the "Designed by HTML Codex" footer link**
(or buy their Credit Removal License: https://htmlcodex.com/credit-removal). See LICENSE.txt.

## Run locally (Windows PowerShell)
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py seed_demo          # SAMPLE content, replace it in /admin
    python manage.py createsuperuser
    python manage.py runserver
Site: http://127.0.0.1:8000  |  Owner panel: http://127.0.0.1:8000/admin

## What the owner manages in /admin
- **Site settings**: gym name, tagline, phone, WhatsApp number (919876543210 format), email, address, hours, social links
- **Plans**, **Trainers** (upload own photos), **Class sessions** (timetable), **Testimonials** (real reviews only; section hides when empty)
- **Trial bookings**: every form submission, with WhatsApp chat link, status (New/Contacted/Joined), CSV export

## Before showing a client
1. Replace ALL seed data (names "Trainer One", prices, WhatsApp number 919999999999, address).
2. Upload real trainer photos. The fallback photos are the template's stock images.
3. Review the page copy (about text in Site settings; feature texts in core/templates/home.html).

## Deploy (Render / Railway)
Build: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
Start: `gunicorn gymsite.wsgi`. Set the env vars from .env.example.
Note: SQLite and uploaded photos need a persistent disk on the host (or switch DATABASES to Postgres).

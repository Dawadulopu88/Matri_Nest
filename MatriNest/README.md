# মাতৃNest — Django Project

A maternal & child healthcare platform: doctor appointments, a medicine
corner, health tracking, and simple service pages (ambulance, emergency,
mental wellness, nurse hire).

## Roles & permissions

| Role    | How it's granted                          | Can do |
|---------|--------------------------------------------|--------|
| Admin   | `is_staff` / `is_superuser` (via `createsuperuser` or the admin panel) | Everything — every page in the app, plus the full Django admin at `/admin/` (manage all users, medicines, appointments, health records). Never granted through the signup form. |
| Doctor  | `user_type = 'doctor'` (chosen at signup)  | Browse medicines, view the full appointment queue (read-only), use the simple service pages (ambulance/emergency/mental/nurse). Cannot add/edit/delete medicines, cannot see other users' health records. |
| Patient | `user_type = 'patient'` (chosen at signup, default) | Browse medicines, book and view their **own** appointments, log and view their **own** health records, use the service pages. Cannot add/edit/delete medicines. |

Permission checks live in `myapp/decorators.py` (`@role_required(...)`).

## Setup

```bash
# from the project folder (the one with manage.py)
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

# create your first admin account
python manage.py createsuperuser

python manage.py runserver
```

Visit `http://127.0.0.1:8000/`. Sign up as a patient or doctor through the
site, or log in with the superuser account to see the admin-only links and
`/admin/` panel.

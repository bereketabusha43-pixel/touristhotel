# Deploying to PythonAnywhere — Step-by-Step Guide

Complete guide for deploying **Arba Minch Tourist Hotel** (Django) to [PythonAnywhere](https://www.pythonanywhere.com).

**Time required:** ~30–45 minutes (first time)

---

## Before you start

You need:

- A [PythonAnywhere](https://www.pythonanywhere.com) account (Beginner free tier works for testing)
- Your project files (upload via Git, or zip upload)
- Your PythonAnywhere **username** (e.g. `johndoe` → site will be `johndoe.pythonanywhere.com`)

**Recommended Python version on PythonAnywhere:** 3.10 or 3.11

---

## Step 1 — Create a PythonAnywhere account

1. Go to [https://www.pythonanywhere.com/registration/register/beginner/](https://www.pythonanywhere.com/registration/register/beginner/)
2. Choose a username — this becomes part of your URL: `https://YOURUSERNAME.pythonanywhere.com`
3. Confirm your email and log in

---

## Step 2 — Upload your project

### Option A — Git (recommended)

Open a **Bash console** on PythonAnywhere (Dashboard → Consoles → Bash):

```bash
cd ~
git clone https://github.com/YOUR-ORG/zebib.git
cd zebib
```

### Option B — Upload a ZIP

1. On your PC, zip the project folder (exclude `env/`, `__pycache__/`, `db.sqlite3`, `.env`)
2. PythonAnywhere → **Files** → upload ZIP to `/home/YOURUSERNAME/`
3. In Bash console:

```bash
cd ~
unzip zebib.zip -d zebib
cd zebib
```

Your project should live at: `/home/YOURUSERNAME/zebib`

---

## Step 3 — Create a virtual environment

In the Bash console:

```bash
cd ~/zebib
mkvirtualenv --python=/usr/bin/python3.10 amth-env

workon amth-env
pip install --upgrade pip
pip install -r requirements-production.txt
```

### If `mysqlclient` fails to install

```bash
pip install mysqlclient
```

If it still fails, use **SQLite** for initial testing (see Step 5 — leave `DB_ENGINE` empty in `.env`).

---

## Step 4 — Create a MySQL database (recommended)

1. Go to **Dashboard → Databases**
2. Click **Create a new database**
3. Choose a name, e.g. `amth_hotel`
4. Note these values (replace `YOURUSERNAME`):

| Setting  | Value |
|----------|-------|
| Host     | `YOURUSERNAME.mysql.pythonanywhere-services.com` |
| Username | `YOURUSERNAME` |
| Database | `YOURUSERNAME$amth_hotel` |
| Password | (set on Databases page) |

> **Important:** The database name uses a **dollar sign** `$`, not underscore: `johndoe$amth_hotel`

---

## Step 5 — Configure environment variables

In Bash:

```bash
cd ~/zebib
cp .env.production.example .env
nano .env
```

Edit `.env` — minimum required changes:

```ini
DJANGO_SETTINGS_MODULE=config.settings.production
SECRET_KEY=paste-a-long-random-string-here
DEBUG=False
ALLOWED_HOSTS=YOURUSERNAME.pythonanywhere.com
SITE_URL=https://YOURUSERNAME.pythonanywhere.com
CSRF_TRUSTED_ORIGINS=https://YOURUSERNAME.pythonanywhere.com

DB_ENGINE=django.db.backends.mysql
DB_NAME=YOURUSERNAME$amth_hotel
DB_USER=YOURUSERNAME
DB_PASSWORD=your-mysql-password-from-step-4
DB_HOST=YOURUSERNAME.mysql.pythonanywhere-services.com
DB_PORT=3306
```

**Generate a secret key:**

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Save the file (`Ctrl+O`, `Enter`, `Ctrl+X` in nano).

---

## Step 6 — Run database setup

```bash
workon amth-env
cd ~/zebib

python manage.py migrate
python manage.py populate_sample_data
python manage.py assign_local_images
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

Or run the helper script:

```bash
bash scripts/post_deploy.sh
python manage.py populate_sample_data
python manage.py createsuperuser
```

---

## Step 7 — Configure the Web app

### 7a. Create a web app (first time only)

1. **Dashboard → Web → Add a new web app**
2. Choose **Manual configuration** (not Django wizard)
3. Select **Python 3.10** (or 3.11)

### 7b. Set virtualenv path

On the Web tab, under **Virtualenv**:

```
/home/YOURUSERNAME/.virtualenvs/amth-env
```

### 7c. Edit WSGI file

Click the **WSGI configuration file** link. Delete its contents and paste from `scripts/pythonanywhere_wsgi.py`, replacing `YOURUSERNAME`:

```python
import os
import sys

path = '/home/YOURUSERNAME/zebib'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.production'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Save (`Ctrl+S`).

### 7d. Static and media files mapping

On the Web tab, scroll to **Static files** and add:

| URL | Directory |
|-----|-----------|
| `/media/` | `/home/YOURUSERNAME/zebib/media/` |

> CSS/JS are served by **WhiteNoise** from `staticfiles/` — no `/static/` mapping needed.

Click **Save**.

---

## Step 8 — Reload and test

1. Click the green **Reload** button on the Web tab
2. Visit: `https://YOURUSERNAME.pythonanywhere.com`
3. Admin: `https://YOURUSERNAME.pythonanywhere.com/admin/`

### Checklist

- [ ] Homepage loads with styles
- [ ] Images appear
- [ ] Admin login works
- [ ] Booking form submits
- [ ] `/robots.txt` and `/sitemap.xml` load

---

## Step 9 — Fix common issues

### 500 Internal Server Error

Check **Web tab → Log files → Error log**, then run:

```bash
workon amth-env
cd ~/zebib
python manage.py check --deploy
```

### Static files (CSS) not loading

```bash
python manage.py collectstatic --noinput
```

Then **Reload** the web app.

### CSRF verification failed

```ini
CSRF_TRUSTED_ORIGINS=https://YOURUSERNAME.pythonanywhere.com
SITE_URL=https://YOURUSERNAME.pythonanywhere.com
```

### DisallowedHost error

```ini
ALLOWED_HOSTS=YOURUSERNAME.pythonanywhere.com
```

### MySQL connection error

- Database name must use `$`: `YOURUSERNAME$amth_hotel`
- Confirm password on Databases tab

### Redirect loop

```ini
SECURE_SSL_REDIRECT=False
```

---

## Step 10 — Updating after code changes

```bash
workon amth-env
cd ~/zebib
git pull
pip install -r requirements-production.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

Then **Reload** on the Web tab.

---

## File reference

| File | Purpose |
|------|---------|
| `.env.production.example` | Production environment template |
| `config/settings/production.py` | Production Django settings |
| `scripts/pythonanywhere_wsgi.py` | WSGI template for Web tab |
| `scripts/post_deploy.sh` | Migrate + collectstatic script |
| `requirements.txt` | Python dependencies |

---

## Security reminders

- Never commit `.env` to Git
- Use a strong `SECRET_KEY` in production
- Change default admin password immediately
- Keep `DEBUG=False` in production

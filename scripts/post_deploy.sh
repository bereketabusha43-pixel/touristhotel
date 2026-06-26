#!/bin/bash
# Post-deployment script for PythonAnywhere
# Run from project root:  bash scripts/post_deploy.sh
set -e

echo "==> Installing dependencies..."
pip install -r requirements-production.txt

echo "==> Running migrations..."
python manage.py migrate --noinput

echo "==> Collecting static files..."
python manage.py collectstatic --noinput

echo "==> Assigning local images (if images/ folder exists)..."
if [ -d "images" ]; then
    python manage.py assign_local_images || true
fi

echo ""
echo "==> Done! Reload your web app on the PythonAnywhere Web tab."
echo "    If first deploy, also run:"
echo "      python manage.py populate_sample_data"
echo "      python manage.py createsuperuser"

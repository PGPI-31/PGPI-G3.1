#!/bin/sh

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Check if database is empty and load data only if necessary
if python manage.py shell -c "from boats.models import BoatModel; print(BoatModel.objects.exists())" | grep -q "False"; then
  echo "Database is empty. Loading initial data..."
  python manage.py loaddata initial_data.json
  echo "Creating admin user..."
  python manage.py create_admin
else
  echo "Database already contains data. Skipping fixture loading."
fi

# Start the application
exec gunicorn safeport.wsgi:application --bind 0.0.0.0:8000
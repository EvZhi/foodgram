ls -a
cd src/
# python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py load_all_data
python manage.py collectstatic --no-input --clear
cp -r /app/collected_static/. /backend_static/static/

gunicorn --bind 0:8080 config.wsgi
ls -a
cd src/
python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py import_ingredients
python manage.py import_tags
python manage.py collectstatic --no-input --clear
python manage.py auto_createsuperuser --username root --email root@ya.ru --password 1234

cp -r /app/collected_static/. /backend_static/static/

gunicorn --bind 0:8080 config.wsgi
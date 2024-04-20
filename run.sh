export FLASK_ENV=development
flask db init
flask db migrate -m "Migrations"
flask db upgrade
python run.py
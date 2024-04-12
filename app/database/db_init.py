from app import create_app, db
from app.auth.models import User  # Import all other models similarly

app = create_app()

with app.app_context():
    db.create_all()

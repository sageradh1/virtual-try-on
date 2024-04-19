from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True )
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    image_path = db.Column(db.String(120), nullable=True)
    gender = db.Column(db.String())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "gender": self.gender,
            "image_path": self.image_path
        }

class GeneratedImage(db.Model):
    id = db.Column(db.Integer, primary_key=True,index=True)
    product_id = db.Column(db.Integer)
    username = db.Column(db.String())
    source_image_path = db.Column(db.String())
    generated_image_path = db.Column(db.String())

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "product_id": self.product_id,
            "source_image_path": self.source_image_path,
            "generated_image_path": self.generated_image_path
        }
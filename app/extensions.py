from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_uploads import UploadSet, IMAGES, configure_uploads

db = SQLAlchemy()
migrate = Migrate()


# photos = UploadSet('photos', IMAGES)
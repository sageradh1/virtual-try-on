from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.vision.synthesis import ImageSynthesiser
from celery import Celery


db = SQLAlchemy()
migrate = Migrate()
synthesiser = ImageSynthesiser()
# synthesiser.preload()
def get_synthesiser():
    return synthesiser


# celery_app = Celery('vto_celery',backend='redis://localhost', broker='redis://localhost')

# @celery_app.task
# def background_synthesis_function(data_dict):

#     clothes = [
#     # f"{current_app.config['CLOTHES_PHOTOS_DEST']}/shirt.jpg"
#     # f"{current_app.config['CLOTHES_PHOTOS_DEST']}/suit.jpeg"
#     '/Users/sagar/working_dir/github_personal/virtual-try-on/app/static/clothes/shirt.jpg'
#     ]

#     for cloth in clothes:
#         data = dict()
#         data['person_image_path'] = data_dict['person_image_path']
#         data['cloth_image_path'] = cloth

#         generated_image=synthesiser.produce_synthesized_image(data)

#         datetime_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
#         new_generated_filename = f"{data_dict['uploaded_filename_ext']}_{datetime_stamp}{data_dict['uploaded_filename_ext']}"
#         generated_file_path = os.path.join('/Users/sagar/working_dir/github_personal/virtual-try-on/app/static/generated', new_generated_filename)
#         generated_image.save(generated_file_path)

#         from app.auth.models import GeneratedImage

#         generated_image = GeneratedImage(
#             username=data_dict['username'],
#             source_image_path=data_dict['person_image_path'],
#             generated_image_path=generated_file_path
#         )
#         db.session.add(generated_image)
#         db.session.commit()
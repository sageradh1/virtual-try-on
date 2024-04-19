# # from celery import Celery

# # celery = Celery(__name__)

# # def make_celery(app):
# #     celery.conf.update(app.config)
# #     return celery



# # from celery import Celery, Task
# # from flask import Flask

# # def celery_init_app(app: Flask) -> Celery:
# #     class FlaskTask(Task):
# #         def __call__(self, *args: object, **kwargs: object) -> object:
# #             with app.app_context():
# #                 return self.run(*args, **kwargs)

# #     celery_app = Celery(app.name, task_cls=FlaskTask)
# #     celery_app.config_from_object(app.config["CELERY"])
# #     celery_app.set_default()
# #     app.extensions["celery"] = celery_app
# #     return celery_app

# from celery import Celery

# def make_celery(app):
#     celery = Celery(
#         app.import_name,
#         backend=app.config['CELERY_RESULT_BACKEND'],
#         broker=app.config['CELERY_BROKER_URL']
#     )
#     celery.conf.update(app.config)
#     return celery

# celery = make_celery(app)


# # from celery import Celery

# # def make_celery(app):
# #     celery = Celery(app.import_name)
# #     celery.conf.update(app.config["CELERY_CONFIG"])

# #     class ContextTask(celery.Task):
# #         def __call__(self, *args, **kwargs):
# #             with app.app_context():
# #                 return self.run(*args, **kwargs)

# #     celery.Task = ContextTask
# #     return celery
from app import create_app
from dotenv import load_dotenv

load_dotenv()
# app, celery_app = create_app()
# app.app_context().push()


app = create_app()

if __name__ == '__main__':
    app.run(use_reloader=False)
#     celery.start()
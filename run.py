from app import create_app
from dotenv import load_dotenv
import os

load_dotenv()

host = os.getenv("HOST", "127.0.0.1")
port = int(os.getenv("PORT", 8081))
app = create_app()

if __name__ == '__main__':
    app.run(host=host, port=port, use_reloader=False)
from app import create_app
from dotenv import load_dotenv
import os

load_dotenv()
app = create_app()

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')
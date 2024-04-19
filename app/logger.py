import logging
import os

if os.getenv('FLASK_ENV') == 'production':
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='./logs/vto_app.log')
else:
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='./logs/vto_app.log')
app_logger = logging.getLogger('vto_flask_app')
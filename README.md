Steps for first run:
1. Create an env
python -m venv venv

2. Activate the environment
source ./venv/bin/activate

3. Upgrade pip and install dependencies
python -m pip install --upgrade pip

4. Install dependency
pip install -r requirements.txt 

5. To run in development
flask --app ./app.py run

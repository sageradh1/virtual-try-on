from flask import Flask, render_template
from blueprints.module_one.module_one import module_one

app = Flask(__name__)
app.register_blueprint(module_one)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=True)
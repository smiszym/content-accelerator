from datetime import datetime
from flask import Flask, render_template

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/')
def hello():
    return render_template(
        'index.html',
        generation_timestamp=str(datetime.now()))

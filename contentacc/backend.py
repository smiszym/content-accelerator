from datetime import datetime
from flask import Flask, render_template, request
from contentacc.content_extraction import extract_content_from_url

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    url = request.args.get('url')
    return render_template(
        'index.html',
        url=url,
        content=extract_content_from_url(url) if url is not None else None)

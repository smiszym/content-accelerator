from flask import Flask, request
from contentacc.content_extraction import extract_content_from_url

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/minimized-page', methods=['GET'])
def minimized_page():
    url = request.args.get('url')
    if url is None:
        return '{"error": "not found"}'
    return extract_content_from_url(url).to_json()

from flask import abort, Flask, request
from flask_gzip import Gzip
from contentacc.content_extraction import extract_content_from_url
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s: %(message)s')


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)
gzip = Gzip(app)


@app.route('/v1/minimized-page', methods=['GET'])
def minimized_page():
    url = request.args.get('url')
    logging.info("Got request for " + url)
    if url is None:
        return '{"error": "not found"}'
    content = extract_content_from_url(url)
    if content is not None:
        response = content.to_json()
        logging.info("Sending response for " + url)
        return response
    else:
        abort(404)

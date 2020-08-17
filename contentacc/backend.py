from flask import abort, Flask, request
from flask_gzip import Gzip
from contentacc.content_extraction import \
    extract_content_from_url, remove_from_caches
import json
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
        abort(404)
    content, metadata = extract_content_from_url(url)
    if content is not None:
        response = json.dumps({
            "cache_used": metadata.cache_used,
            "title": content.title,
            "text": content.text,
        })
        logging.info("Sending response for " + url)
        return response
    else:
        abort(404)


@app.route('/v1/minimized-page', methods=['DELETE'])
def minimized_page_deleter():
    url = request.args.get('url')
    logging.info("Got request to delete from cache: " + url)
    if url is None:
        abort(404)
    remove_from_caches(url)
    return "OK"

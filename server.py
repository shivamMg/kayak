import json

from sanic import Sanic
from sanic.exceptions import NotFound, ServerError
from sanic.response import (json as json_response, html as html_response, text
                            as text_response)

from kayak.auth import TwitterOAuth2
from kayak.kayak import KayakSearch
from kayak.utils import KayakError

app = Sanic(__name__)

# Serve static directory
app.static('/static', './site/static')

# Cache `./site/index.html`
with open('./site/index.html', 'r') as handle:
    INDEX_PAGE = handle.read()


# Handle Sanic NotFound exception
@app.exception(NotFound)
def handle_notfound(request, exception):
    return text_response('Resource not found.')


# Handle Sanic ServerError exception
@app.exception(ServerError)
def handle_servererror(request, exception):
    return text_response('Something bad happened.')


# Handle Kayak's error
@app.exception(KayakError)
def handle_apierror(request, exception):
    error = {'error': dict(message=str(exception))}
    return json_response(error, status=500)


@app.route('/', methods=['GET'])
async def index(request):
    return html_response(INDEX_PAGE)


@app.route('/api', methods=['GET'])
async def api(request):
    hashtag = request.args.pop('hashtag', [])
    max_id = request.args.pop('max_id', [])

    if not hashtag:
        error = {'error': dict(message='`hashtag` parameter is required')}
        return json_response(error, status=400)

    # If not empty use the first value
    if hashtag:
        hashtag = hashtag.pop(0)
    if max_id:
        max_id = int(max_id.pop(0))

    response = api_obj.get_tweets(hashtag, max_id=max_id)

    return json_response(response)


if __name__ == '__main__':
    print('Extracting secrets...')
    try:
        with open('secrets.json', 'r') as handle:
            SECRETS = json.load(handle)
    except IOError:
        raise IOError('`secrets.json` not found.')

    consumer_key = SECRETS.get('consumer_key', '')
    consumer_secret = SECRETS.get('consumer_secret', '')

    auth_obj = TwitterOAuth2(consumer_key, consumer_secret)
    print('Requesting access token...')
    auth_obj.request_token()
    print('Access token:', auth_obj.access_token)

    api_obj = KayakSearch(auth_obj)

    app.run(host='0.0.0.0', port=SECRETS.get('server_port', 8080))

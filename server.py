import json

from sanic import Sanic
from sanic.exceptions import NotFound, ServerError
from sanic.response import (
    json as json_response,
    html as html_response,
    text as text_response
)

from kayak.auth import TwitterOAuthApi
from kayak.api import TwitterSearchApi
from kayak.utils import APIError as KayakAPIError

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


# Handle Kayak module's APIError
@app.exception(KayakAPIError)
def handle_apierror(request, exception):
    response = exception.to_dict()
    return json_response(response, status=500)


@app.route('/', methods=['GET'])
async def index(request):
    return html_response(INDEX_PAGE)


@app.route('/api', methods=['GET'])
async def api(request):
    hashtag = request.args.pop('hashtag', None)
    since_id = request.args.pop('since_id', None)

    tweet_list = api_obj.get_query_tweets(
        hashtag=hashtag, since_id=since_id)

    return json_response(tweet_list)


if __name__ == '__main__':
    print('Extracting secrets...')
    try:
        with open('secrets.json', 'r') as handle:
            SECRETS = json.load(handle)
    except IOError:
        raise IOError('`secrets.json` not found.')

    consumer_key = SECRETS.get('consumer_key', '')
    consumer_secret = SECRETS.get('consumer_secret', '')

    auth_obj = TwitterOAuthApi(consumer_key, consumer_secret)
    print('Setting access token...')
    auth_obj.set_access_token()

    api_obj = TwitterSearchApi(auth_obj)

    app.run(host='0.0.0.0', port=8080)

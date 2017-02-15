## Kayak

The `kayak` module contains the Twitter Authentication and REST API logic. It's written without any SDKs. Idea was to have separate classes for Twitter OAuth2 and REST APIs. The REST API class contains just the Search Tweets method (since it was the only requirement) and can be augmented by adding methods for other endpoints. The Kayak Search extends REST API class and uses the Search method to implement the required functionality: "Fetch and display Tweets that have been re-Tweeted at least once and contain a particular hashtag".

The `kayak` module is divided into three parts:

#### Authentication (`kayak/auth.py`)

The `TwitterOAuth2` class implements [Application Only Authentication](https://dev.twitter.com/oauth/application-only). A Consumer Key and a Consumer Secret must be provided during initialization. These can be obtained after registering an app at https://apps.twitter.com. Request for Bearer token is not immediately sent. The class provides two methods and a property:

- `request_token()`: Requests Access token from the Twitter server and sets the `access_token` attribute. Also returns the access token value.
- `revoke_token()`: Invalidates the Access token and sets `access_token` to an empty string. Also returns the invalidated token value.
- `bearer_credentials`: Getter for Bearer credentials required for requesting tokens.

#### REST API (`kayak/api.py`)

The Bearer token is used to make requests to different [REST APIs](https://dev.twitter.com/rest/reference). The `TwitterRestApi` class implements the same. Method for [Search API](https://dev.twitter.com/rest/reference/get/search/tweets) endpoint has been implemented. `search_tweet` method lets you search for queries with other parameters as described in the documentation.

#### Kayak Search (`kayak/kayak.py`)

`KayakSearch` class extends `TwitterRestApi` class and uses it's Search method to accomplish the following: "Fetch and display Tweets that have been re-Tweeted at least `some number` of times and contain a particular hashtag". If the access token expires in between calls and new token is requested to make the call again. All this provided by the following method:

```python
get_tweets(self, hashtag, max_id=None, result_type='mixed',
           count=15, retweet_count=1)
```

#### Utilities (`kayak/utils.py`)

Definitions for Exceptions and API URLs used by the module.

### Demo site

The demo site uses the `kayak` module to fetch tweets. The server is written using Sanic Framework. `kayak` itself uses just the `requests` package, and Sanic Framework is used only for the demo site.

#### Server (`server.py`)

- Provides `/api` endpoint to fetch tweets containing a particular hashtag.
- Renders a simple app at root to let users use the API.

### Instructions

Create a virtual environment and install requirements. You're going to need Python3.5+ for the Sanic framework.

```bash
python3 -m venv venv
# or virtualenv -p `which python3` venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `secrets.json` file containing your Twitter application Consumer Key and Secret. You can also specify the server port in the same file.

```json
{
    "consumer_key": "insert-consumer-key",
    "consumer_secret": "insert-consumer-secret",
    "server_port": 8080
}
```

If not specified, the server runs on port 8080.


Inside the virtual environment run the server through `server.py`:

```bash
python server.py
```


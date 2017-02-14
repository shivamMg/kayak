## Kayak

The `kayak` module contains the Twitter API wrapper logic. It's written without any SDKs. Idea was to separate Twitter OAuth from Search API and provide an easy way to make requests and fetch required Tweets. It's divided into two parts:

#### Authentication (`kayak/auth.py`)

Twitter APIs require a valid Bearer token for making requests to its APIs. The `TwitterOAuthApi` class implements the [Application Only Authentication](https://dev.twitter.com/oauth/application-only). A Consumer Key and a Consumer Secret must be provided during initialization. These can be obtained after registering an app at https://apps.twitter.com. Request for Bearer token is not immediately sent. It must be done by executing `set_access_token` method on the instance.

#### Tweets Search API (`kayak/api.py`)

The Bearer token obtained after successful authentication is used to make requests to the [Search API](https://dev.twitter.com/rest/reference/get/search/tweets). The `TwitterSearchApi` class implements the same. It requires the Bearer token for instance initialization. `search_tweets` method is wrapper to the API. `get_query_tweets`  method provides the required functionality (display Tweets that have been re-Tweeted at least once and contain the hashtag #custserv). It is an abstraction over `search_tweets` method and provides parameter to search for any hashtag.

### Demo site

The demo site uses the `kayak` module to fetch tweets. The server is written using Sanic Framework. `kayak` itself uses just the `requests` package, and Sanic Framework is used only for the demo site.

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


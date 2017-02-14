import requests

from .utils import SEARCH_TWEETS_URL, APIError


class TwitterSearchApi:
    """
    Twitter Tweet Search API wrapper.
    API Docs: https://dev.twitter.com/rest/reference/get/search/tweets

    Instance of this class requires an Auth object that contains a valid
    API Access token in `access_token` attribute. Auth object could be an
    instance of the `TwitterOAuthApi` class.
    """
    def __init__(self, auth_obj):
        """
        Parameters:
        `auth_obj`: Object that has an `access_token` attribute.
        """
        self.access_token = auth_obj.access_token

    def search_tweets(self, **options):
        """
        Requests the Search Tweets API endpoint with `options`. Documentation
        for the endpoint is available at the API Docs.
        Returns response in a dictionary.

        `options` must contain the required query key `q`.

        Uses the Bearer token (`self.access_token`) in the Authorization
        header.

        Exceptions generated by `requests` module must be handled separately.
        """
        # Check for query key `q`
        if not options.get('q', False):
            raise Exception('Query key `q` is required in `options`.')

        headers = {'Authorization': 'Bearer {}'.format(self.access_token)}
        payload = options

        response = requests.get(
            SEARCH_TWEETS_URL, params=payload, headers=headers)

        if response.status_code != requests.codes.ok:
            raise APIError('Invalid bearer token.')

        return response.json()

    def get_query_tweets(self, hashtag=None, since_id=None):
        """
        Returns Tweets that contain the hashtag `hashtag` :P and that have ids
        that come after `since_id`. Also, it filters out tweets that have
        retweet_count less than 1.
        """
        if not hashtag:
            raise APIError('`hashtag` parameter is required.')

        options = {
            'q': '%23{}'.format(hashtag),
            'since_id': since_id
        }
        # If `since_id` is None, remove it from options
        if not since_id:
            options.pop('since_id')

        response = self.search_tweets(**options)

        status_list = response.get('statuses', [])
        tweet_list = []
        for status in status_list:
            if status.get('retweet_count') >= 1:
                tweet_list.append({
                    'text': status['text'],
                    'user': status['user']['screen_name'],
                    'date': status['created_at'],
                    'retweetCount': status['retweet_count']
                })

        return tweet_list
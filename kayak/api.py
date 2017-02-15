import requests
from requests.exceptions import RequestException

from .utils import SEARCH_TWEETS_URL, KayakError, InvalidTokenError, \
    FailedRequestError


class TwitterRestApi:
    """
    Twitter REST API wrapper.
    API Docs: https://dev.twitter.com/rest/public

    Instance of this class requires an Auth object that must contain a valid
    API Access token (in `access_token` attribute) for successful requests.
    Auth object could be an instance of the `TwitterOAuth2` class.
    """

    def __init__(self, auth_obj):
        """
        Parameters:
        `auth_obj`: Object must have `access_token` attribute.
        """
        self.auth_obj = auth_obj

    @property
    def access_token(self):
        return self.auth_obj.access_token

    def search_tweets(self, **options):
        """
        Requests the Search Tweets API endpoint with `options`. Documentation
        for the endpoint is available at:
        https://dev.twitter.com/rest/reference/get/search/tweets

        Returns json encoded content of response.
        """
        # Check for required query parameter `q`
        if not options.get('q', False):
            raise Exception('`options` must contain query key `q`.')

        headers = {'Authorization': 'Bearer {}'.format(self.access_token)}

        try:
            response = requests.get(
                SEARCH_TWEETS_URL, params=options, headers=headers, timeout=5)
        except RequestException:
            raise FailedRequestError

        if response.status_code != requests.codes.ok:
            # Check for Invalid or expired token (Code 89)
            # https://dev.twitter.com/overview/api/response-codes
            error_list = response.json()
            for error in error_list:
                if error.code == 89:
                    raise InvalidTokenError

            # Use first error message
            raise KayakError(error_list[0].message)

        return response.json()

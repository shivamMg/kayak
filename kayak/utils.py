# Official Twitter API URLs

TWITTER_API_BASE = 'https://api.twitter.com'
OAUTH2_TOKEN_URL = '{}/oauth2/token'.format(TWITTER_API_BASE)
SEARCH_TWEETS_URL = '{}/1.1/search/tweets.json'.format(TWITTER_API_BASE)


# Errors and Exceptions

class KayakError(Exception):
    """
    Generic exception for kayak module.
    """
    pass


class FailedRequestError(KayakError):
    """
    Exception for failed requests to Twitter URLs.
    """
    def __init__(self):
        message = 'Failed Twitter request.'
        super().__init__(message)


class InvalidTokenError(Exception):
    """
    Exception for Invalid or expired access token.
    """
    pass

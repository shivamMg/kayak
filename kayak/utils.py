# Official Twitter API URLs
TWITTER_API_BASE = 'https://api.twitter.com'
OAUTH2_TOKEN_URL = '{}/oauth2/token'.format(TWITTER_API_BASE)
SEARCH_TWEETS_URL = '{}/1.1/search/tweets.json'.format(TWITTER_API_BASE)


# API Error
class APIError(Exception):
    """
    Custom error for exceptions raised through `TwitterOAuthApi` and
    `TwitterSearchApi`.
    """
    def to_dict(self):
        """
        Helper method to return error dictionary that can be serialized as
        JSON for responses.
        """
        return {'error': {'message': self.message}}

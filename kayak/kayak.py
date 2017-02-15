from .api import TwitterRestApi
from .utils import InvalidTokenError


class KayakSearch(TwitterRestApi):
    """
    Inherits from `TwitterRestApi` class.
    Provides `get_tweets` method to search for tweets with a particular hashtag
    and minimum retweet count.
    """

    def get_tweets(self,
                   hashtag,
                   max_id=None,
                   result_type='mixed',
                   count=15,
                   retweet_count=1):
        """
        Returns Tweets that contain the hashtag `hashtag`.
        Minimum retweet count can be set through `retweet_count` parameter.
        """
        options = {
            'q': '#{}'.format(hashtag),
            'max_id': max_id,
            'result_type': result_type,
            'count': count
        }
        # If `max_id` is None, remove it from options
        if not max_id:
            options.pop('max_id')

        try:
            response = self.search_tweets(**options)
        except InvalidTokenError:
            # Request a new access token
            self.auth_obj.request_token()
            # Search tweets again
            response = self.search_tweets(**options)

        status_list = response.get('statuses', [])
        tweet_list = []
        # Initialize max_id
        if len(status_list) > 0:
            max_id = status_list[0]['id']
        else:
            max_id = 0

        # Select all tweets with retweet count at least equal to
        # `retweet_count`
        for status in status_list:
            if status.get('retweet_count') >= 1:
                tweet_list.append({
                    'idStr': status['id_str'],
                    'text': status['text'],
                    'user': status['user']['screen_name'],
                    'date': status['created_at'],
                    'retweetCount': status['retweet_count']
                })

            # Keep track of the lowest id so not to request
            # already obtained tweets again
            if status['id'] < max_id:
                max_id = status['id']

        return {'tweets': tweet_list, 'meta': {'maxId': max_id}}

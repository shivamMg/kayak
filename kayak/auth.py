from urllib.parse import quote_plus
from base64 import b64encode

import requests

from .utils import OAUTH2_TOKEN_URL, APIError


class TwitterOAuthApi:
    """
    Twitter OAuth API wrapper for Application-Only Authentication.
    API Docs: https://dev.twitter.com/oauth/application-only

    Instance of this class requires a Consumer Key and Consumer Secret for
    initiation. Both can be obtained after registering an application at
    https://apps.twitter.com.

    Access token is not immediately requested for an instance. This has to be
    done by calling `set_access_token` method on the object.

    Methods below follow the Twitter API documentation for obtaining access
    token.
    """
    def __init__(self, consumer_key, consumer_secret):
        """
        Parameters:
        `consumer_key`: Consumer Key for the Twitter App.
        `consumer_secret`: Consumer Secret for the Twitter App.
        """
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = ''

    def _get_encoded_cred(self):
        """
        Returns Base64 encoded credential.
        Urlencodes both `self.consumer_key` and `self.consumer_secret`, and
        calculates credential. The credential must be Base64 encoded as per
        the API documentation.
        """
        encoded_ck = quote_plus(self.consumer_key)
        encoded_cs = quote_plus(self.consumer_secret)
        # Credential format as defined in API Docs
        credential = '{}:{}'.format(encoded_ck, encoded_cs)
        b64credential = b64encode(credential.encode('ascii'))
        return b64credential.decode('ascii')

    def set_access_token(self):
        """
        Sets `self.access_token` using Base64 encoded credential.

        Requests the Twitter OAuth API server for the access token. In case of
        invalid credentials or invalid token type an Exception is raised.

        Exceptions generated by `requests` module must be handled separately.
        """
        credential = self._get_encoded_cred()
        headers = {
            'Authorization': 'Basic {}'.format(credential),
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }
        data = 'grant_type=client_credentials'

        response = requests.post(
            OAUTH2_TOKEN_URL, data=data, headers=headers, timeout=5)

        if response.status_code != requests.codes.ok:
            raise APIError('Invalid credentials. Could not get bearer token.')

        response_body = response.json()
        if response_body.get('token_type', '') == 'bearer':
            self.access_token = response_body.get('access_token')
        else:
            raise APIError(('Invalid token type of returned token. Token type')
                           ('is not bearer.'))

    def invalidate_access_token(self):
        """
        Invalidates `self.access_token`.
        """
        # TODO
        pass

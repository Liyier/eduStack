from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication


class MyAuthentication(BaseAuthentication):
    """自己的验证类"""
    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        """
        token = "random string"
        user = "liyi from db"
        if token is True:
            request.user = user
            request.auth = token
        else:
            raise exceptions.AuthenticationFailed("用户未登陆")

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        pass

from rest_framework import authentication


class JWTAuthBackend(authentication.BaseAuthentication):
    def authenticate(self, request):
        from mad.app.services import AuthService

        token = request.META.get("HTTP_AUTHORIZATION")
        if not token:
            return None

        user = AuthService.factory().execute(token)
        return user, None

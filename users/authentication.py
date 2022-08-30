from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings


class JWTCookieAuthentication(JWTAuthentication):

    def authenticate(self, request):
        cookie_name = getattr(settings, 'JWT_AUTH_COOKIE', None)

        header = self.get_header(request)
        if header is None:
            if cookie_name:
                raw_token = request.COOKIES.get(cookie_name)

            else:
                return None

        else:
            raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token), validated_token

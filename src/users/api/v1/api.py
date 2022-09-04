from rest_framework import permissions, generics
from rest_framework.views import APIView
from django.contrib.auth import login as session_login, logout

from ...models import Review
from ...util import (
    jwt_encode, set_cookie_jwt, set_cookie_jwt_refresh,
    set_cookie_jwt_access, unset_cookie_jwt, sensitive_post_parameters_m
)
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
from .serializers import (
    UserSerializer, JWTSerializer, LoginSerializer, RegisterSerializer,
    PasswordResetSerializer, PasswordChangeSerializer, ReviewSerializer,
    TokenRefreshCookieSerializer, PasswordResetCompleteSerializer, UserProfileSerializer
)
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenRefreshView
from .permissions import IsReviewOwner
from django.db.backends.base.base import DatabaseError
from rest_framework.exceptions import NotAcceptable


User = get_user_model()


class HostRegisterView(generics.CreateAPIView):

    @sensitive_post_parameters_m
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
    throttle_scope = 'auth'

    def get_response(self, user, access_token, refresh_token, headers):

        data = {
            'user': user,
            'access_token': access_token,
            'refresh_token': refresh_token
        }

        response_serializer = JWTSerializer(data, context=self.get_serializer_context())
        response = Response(response_serializer.data, status.HTTP_201_CREATED, headers=headers)

        if getattr(settings, 'AUTH_USE_COOKIE', False):
            set_cookie_jwt(response, access_token, refresh_token)

        if getattr(settings, 'SESSION_AUTH', False):
            session_login(self.request, user)

        return response

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        refresh_token, acc_token = jwt_encode(user)

        return self.get_response(user, acc_token, refresh_token, headers)

    def perform_create(self, serializer):
        user = serializer.save(role=User.Roles.HOST)
        return user


class GuestRegisterView(HostRegisterView):

    def perform_create(self, serializer):
        user = serializer.save(role=User.Roles.GUEST)
        return user


class UserDetail(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.defer('password', 'is_active', 'is_staff', 'date_joined')
    throttle_scope = 'auth'

    lookup_field = 'uuid'


class UserProfile(generics.RetrieveAPIView, generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    queryset = User.objects.defer('password', 'is_active', 'is_staff', 'date_joined')

    def get_object(self):
        return self.request.user


class LoginView(generics.GenericAPIView):

    @sensitive_post_parameters_m
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    throttle_scope = 'auth'

    refresh_token = None
    access_token = None
    user = None

    def login(self):
        self.user = self.serializer.validated_data['user']
        self.refresh_token, self.access_token = jwt_encode(self.user)
        if getattr(settings, 'SESSION_AUTH', False):
            session_login(self.request, self.user)

    def get_response(self):
        response_data = {'user': self.user,
                         'access_token': self.access_token,
                         'refresh_token': self.refresh_token}

        response_serializer = JWTSerializer(response_data)

        response = Response(response_serializer.data, status=status.HTTP_200_OK)

        if getattr(settings, 'AUTH_USE_COOKIE', False):
            set_cookie_jwt(response, self.access_token, self.refresh_token)

        return response

    def post(self, request, *args, **kwargs):
        print(self.request.version)

        self.serializer = self.get_serializer(data=request.data)
        self.serializer.is_valid(raise_exception=True)

        self.login()
        return self.get_response()


class RefreshTokenView(TokenRefreshView):
    serializer_class = TokenRefreshCookieSerializer
    throttle_scope = 'auth'

    def finalize_response(self, request, response, *args, **kwargs):

        if response.status_code == 200 and 'access' in response.data:
            set_cookie_jwt_access(response, response.data['access'])

        if response.status_code == 200 and 'refresh' in response.data:
            set_cookie_jwt_refresh(response, response.data['refresh'])

        return super().finalize_response(request, response, *args, **kwargs)


class LogoutView(APIView):
    throttle_scope = 'auth'

    def post(self, request, *args, **kwargs):

        response = Response({'detail': 'Logged out successfully'}, status.HTTP_200_OK)
        unset_cookie_jwt(response)

        if getattr(settings, 'SESSION_AUTH', False):
            logout(self.request)

        return response


class PasswordChangeView(generics.GenericAPIView):

    @sensitive_post_parameters_m
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    throttle_scope = 'auth'


    serializer_class = PasswordChangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response({'detail': 'password changed successfully'}, status.HTTP_200_OK)


class PasswordResetView(generics.GenericAPIView):

    @sensitive_post_parameters_m
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    serializer_class = PasswordResetSerializer
    permission_classes = [permissions.AllowAny]
    throttle_scope = 'auth'

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response({'detail': 'password reset email sent to you'}, status.HTTP_200_OK)


class ResetPasswordConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetCompleteSerializer
    permission_classes = [permissions.AllowAny]
    throttle_scope = 'auth'

    @sensitive_post_parameters_m
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response({'detail': 'password change successfully'}, status.HTTP_200_OK)


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except DatabaseError:
            raise NotAcceptable('you cant vote again.')


class ReviewDetail(generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewOwner]

    queryset = Review.objects.all()

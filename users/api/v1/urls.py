from django.urls import path
from . import api
from rest_framework_simplejwt.views import TokenVerifyView, TokenObtainPairView

urlpatterns = [
    path('register/', api.RegisterView.as_view(), name='register'),
    path('user/<uuid:uuid>/', api.UserDetail.as_view(), name='user-detail'),
    path('profile/', api.UserProfile.as_view(), name='profile'),

    path('login/', api.LoginView.as_view(), name='login'),
    path('logout/', api.LogoutView.as_view(), name='logout'),

    path('token/refresh/', api.RefreshTokenView.as_view(), name='refresh_token'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/obtain/', TokenObtainPairView.as_view(), name='obtain_token'),

    path('password/change/', api.PasswordChangeView.as_view(), name='password_change'),
    path('password/reset/', api.PasswordResetView.as_view(), name='password_reset'),

    path('password/reset/confirm/<str:uid>/<str:token>/',
         api.ResetPasswordConfirmView.as_view(),
         name='password_reset_confirm'
         ),
]

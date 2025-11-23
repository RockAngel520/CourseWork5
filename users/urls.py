from django.urls import path
from rest_framework.permissions import AllowAny

from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserRetrieveAPIView, UserUpdateAPIView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = UsersConfig.name

urlpatterns = [
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("<int:pk>/", UserRetrieveAPIView.as_view(), name="profile"),
    path("<int:pk>/update/", UserUpdateAPIView.as_view(), name="users_update"),
]

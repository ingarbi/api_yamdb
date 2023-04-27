from django.urls import include, path

from .views import UserViewSet, get_jwt_token, register
from .utils import NoPutRouter

app_name = "api"

router = NoPutRouter()

router.register("users", UserViewSet, basename="users")

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/auth/signup/", register, name="register"),
    path("v1/auth/token/", get_jwt_token, name="token"),
]

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserSignupAPIView, TokenAPIView

app_name = "api"

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/auth/signup/", UserSignupAPIView.as_view(), name="signup"),
    path("v1/auth/token/", TokenAPIView.as_view(), name="token_obtain"),
]

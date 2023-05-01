from django.urls import include, path

from .utils import NoPutRouter
from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    UserViewSet,
    get_jwt_token,
    register,
)

app_name = "api"

router_v1 = NoPutRouter()
router_v1.register("categories", CategoryViewSet)
router_v1.register("genres", GenreViewSet)
router_v1.register("titles", TitleViewSet)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews",
    ReviewViewSet, basename="reviews"
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)
router_v1.register("users", UserViewSet, basename="users")

auth_urlpatterns = [
    path("signup/", register, name="register"),
    path("token/", get_jwt_token, name="token"),
]

urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path("v1/auth/", include(auth_urlpatterns)),
]

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

router = NoPutRouter()
router.register("categories", CategoryViewSet)
router.register("genres", GenreViewSet)
router.register("titles", TitleViewSet)
router.register(
    r"titles/(?P<title_id>\d+)/reviews",
    ReviewViewSet, basename="reviews"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)
router.register("users", UserViewSet, basename="users")

auth_urlpatterns = [
    path("signup/", register, name="register"),
    path("token/", get_jwt_token, name="token"),
]

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/auth/", include(auth_urlpatterns)),
]

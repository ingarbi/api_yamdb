from django.urls import include, path
from .views import UserViewSet, get_jwt_token, register, CategoryViewSet, GenreViewSet, TitleViewSet, ReviewViewSet, CommentViewSet
from .utils import NoPutRouter

app_name = "api"
 
router = NoPutRouter()
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register("users", UserViewSet, basename="users")

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/auth/signup/", register, name="register"),
    path("v1/auth/token/", get_jwt_token, name="token"),
]

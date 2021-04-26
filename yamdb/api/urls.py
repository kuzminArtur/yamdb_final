from rest_framework import routers

from . import views

router_v1 = routers.DefaultRouter()

router_v1.register(
    r'v1/titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet, basename='review'
)
router_v1.register(
    r'v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet, basename='comment'
)
router_v1.register(r'v1/categories', views.CategoryViewSet,
                   basename='categories')
router_v1.register(r'v1/genres', views.GenreViewSet, basename='genres')
router_v1.register(r'v1/titles', views.TitleViewSet, basename='titles')

urlpatterns = router_v1.urls

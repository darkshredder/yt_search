from django.urls import include, path
from rest_framework import routers
from api.views import YTSeachQueryListCreateAPIView, YTSearchResultListAPIView

# router = routers.DefaultRouter()
# router.register(r'yt_search_queries', YTSeachQueryListCreateAPIView.as_view())

urlpatterns = [
    path('yt_search_queries/', YTSeachQueryListCreateAPIView.as_view(), name='yt_search_queries'),
    path('yt_search_results/', YTSearchResultListAPIView.as_view(), name='yt_search_results'),
]
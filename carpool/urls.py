
from .views import PoolsDetailView, poolsListView
from django.urls import path, include, re_path
from rest_framework import routers
router = routers.SimpleRouter()

urlpatterns = [
    path("pools/<int:id>/", PoolsDetailView.as_view(), name='Pools_detail')
]
router.register('pools', poolsListView, basename='PoolsModelGetALL')
urlpatterns += router.urls
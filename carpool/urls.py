
from .views import poolsListView
from django.urls import path, include, re_path
from rest_framework import routers
router = routers.SimpleRouter()

urlpatterns = [

]
router.register('pools', poolsListView, basename='PoolsModelGetALL')
urlpatterns += router.urls
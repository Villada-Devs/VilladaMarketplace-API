from posixpath import basename
from rest_framework import routers
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views.booksView import BookViewSet
from .views.clothesView import ClothViewSet
from .views.toolView import ToolViewSet
from .views.myPostView import MyPostsViewset

router = DefaultRouter()

router.register(r'books', BookViewSet, basename='books_router') # aca definimos una ruta
router.register(r'clothes', ClothViewSet, basename='clothes_router')
router.register(r'tools', ToolViewSet, basename='tools_router')

router.register(r'myposts', MyPostsViewset, basename='myposts_router')

urlpatterns = []
urlpatterns += router.urls 

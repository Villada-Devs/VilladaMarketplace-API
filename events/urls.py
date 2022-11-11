
from .views import EventsViewSet, EventsDetailView
from django.urls import path
from rest_framework import routers

router = routers.SimpleRouter()


urlpatterns =[
    path("events/<int:id>/", EventsDetailView.as_view(), name='Events_detail'),

]

router.register('events', EventsViewSet, basename='EventsModelGetALL')
urlpatterns += router.urls
from rest_framework import serializers
from .models import Event

#UPF API

class EventsSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="created_by.username", read_only=True)
    class Meta:
        model = Event
        fields = ['id','author','title', 'body', 'created_date','image', 'event_date']
        
from rest_framework import serializers
from .models import Pool

class poolsSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="created_by.username", read_only=True)       
    class Meta:
        model = Pool
        exclude = ['created_by']

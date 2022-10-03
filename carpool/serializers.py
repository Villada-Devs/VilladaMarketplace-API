from xmlrpc.client import ResponseError
from rest_framework import serializers
from .models import Pool

class poolsSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="created_by.username", read_only=True)    
       
    class Meta:
        model = Pool
        exclude = ['created_by']


    def validate_alternative_tel(self, data):
        first_tel = self.initial_data['first_tel']
        if data == first_tel:
            raise serializers.ValidationError({"Error": "The secondary cellphone can not be the same as principal "})
        return data

        
from xmlrpc.client import ResponseError
from rest_framework import serializers
from .models import Pool

class poolsSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="created_by.username", read_only=True)       
    class Meta:
        model = Pool
        exclude = ['created_by']

    #validar numero de telefono (mas de 10 digitos)
    def validate_first_tel(self, data):
        if len(str(data)) != 10 :
            raise serializers.ValidationError({"Error": "This phone number is not valid, send 10 digits tel"})
        
        return data
        
        
    def validate_alternative_tel(self, data):
        first_tel = self.initial_data['first_tel']
        if len(str(data)) != 10 :
            raise serializers.ValidationError({"Error" : "This phone number is not valid, send 10 digits tel"})

        if data == first_tel:
            raise serializers.ValidationError({"Error": "The secondary cellphone cant be the same as the first one"})
       
        return data

        
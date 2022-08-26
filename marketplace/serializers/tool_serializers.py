from rest_framework import serializers

from ..models import Tool

class ToolSerializer(serializers.ModelSerializer):

    def validate_tel(self, data):
        if len(str(data)) == 10:
            return data
        else:
            raise serializers.ValidationError({"Este numero de telefono no es valido": "This phone number don't exists"})

    class Meta:
        model = Tool
        exclude = ('on_circulation','created_by')


    def to_representation(self, instance):

        return {
            'id':instance.id,
            'tool':instance.tool,
            'status':instance.status,
            'description':instance.description,
            'price':instance.price,
            'tel':instance.tel, 
            'created_by':instance.created_by.username,
            'creation_date':instance.creation_date
        }

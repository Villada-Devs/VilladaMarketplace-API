from rest_framework import serializers

from ..models import Tool

class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        exclude = ('on_circulation',)


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
from rest_framework import serializers

from ..models import Clothing

class ClothSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clothing
        exclude = ('on_circulation',)

    def to_representation(self, instance):

        return {
            'id':instance.id,
            'type_of_garment':instance.type_of_garment,
            'size':instance.size,
            'status':instance.status,
            'description':instance.description,
            'price':instance.price, 
            'tel':instance.tel,
            'created_by':instance.created_by.username,
            'creation_date':instance.creation_date
        }
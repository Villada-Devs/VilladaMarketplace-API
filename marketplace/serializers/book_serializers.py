from calendar import c
from rest_framework import serializers

from ..models import Book, ImagesBook


class ImagesBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagesBook
        fields = ['image']



class BookSerializer(serializers.ModelSerializer):

    def validate_tel(self, data):
        print(data)
        if len(str(data)) == 10:
            return data
        else:
            raise serializers.ValidationError({"Este numero de telefono no es valido": "This phone number don't exists"})


    """def validate(self, data):
        if len(str(data['tel'])) == 10:
            return data                                 # esto hace lo mismo que el de arriba pero queria mostrar que despues del validate arriba si le pones el dato ya te lo trae solo a ese dato
        else:
            raise serializers.ValidationError({"tel": "This phone number don't exists"})
"""
            
    #imagesbook = serializers.StringRelatedField(many=True)
    #imagesbook = ImagesBookSerializer(many=True)

    class Meta:
        model = Book
    
        fields = ['id','title','imagesbook','author','matter', 'age', 'editorial', 'status', 'price', 'tel', 'creation_date']

  
    def to_representation(self, instance):
        return {
            'id':instance.id,
            'title':instance.title,
            #'imagesbook':instance.imagesbook,
            'author':instance.author,
            'matter':instance.matter,
            'age_of_book':instance.age,
            'editorial':instance.editorial, 
            'status':instance.status,
            'price':instance.price,
            'tel':instance.tel,
            'created_by':instance.created_by.username,
            'creation_date':instance.creation_date
        }

    
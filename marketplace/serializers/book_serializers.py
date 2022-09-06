from calendar import c
from rest_framework import serializers

from ..models import Book, ImagesBook



class ImagesBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImagesBook
        fields = [
            'image'
             ]



class BookSerializer(serializers.ModelSerializer):

    created_by_id = serializers.IntegerField(required=False)
    published_date = serializers.DateField(required = False)


    def validate_tel(self, data):
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
            
    
    imagesbook = ImagesBookSerializer(many=True)

    

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'subject',
            'course',
            'editorial',
            'status',
            'price',
            'tel',
            'created_by_id',
            'creation_date',
            'published_date',
            'imagesbook',
            ] 

    def create(self, validated_data):

        imagesbook_data = validated_data.pop('imagesbook')
        book = Book.objects.create(**validated_data)

        for imagebook_data in imagesbook_data:
            ImagesBook.objects.create(book=book, **imagebook_data)

        return book 
        

"""
{
    "title": "TEST 1",
    "author": "gaston",
    "subject": "lengua",
    "course": "6 Año",
    "editorial": "",
    "status": "Casi nuevo",
    "price": 88888,
    "tel": 3517059561,
    "imagesbook": [
        {
            "image": "/home/gaston/Imágenes/test.png"
        }
    ]
}
"""
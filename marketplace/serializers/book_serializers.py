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

    def validate_tel(self, data):
        if len(str(data)) == 10:
            return data
        else:
            raise serializers.ValidationError({"Error": "This phone number is not valid, send 10 digits tel"})
            

    created_by_id = serializers.IntegerField(required=False)
    published_date = serializers.DateField(required = False)


    imagesbook = ImagesBookSerializer(many=True, read_only =True)
    uploaded_images = serializers.ListField(child = serializers.FileField(max_length = 1000000, allow_empty_file = False, use_url = False), write_only = True) # crea un array en donde se van a meter cosas
    
    
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
            'uploaded_images',
            ] 

    
    def create(self, validated_data):

        uploaded_data = validated_data.pop('uploaded_images')
        book = Book.objects.create(**validated_data)

        for uploaded_item in uploaded_data:
            ImagesBook.objects.create(book=book, image= uploaded_item)
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
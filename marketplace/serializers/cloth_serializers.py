from rest_framework import serializers

from ..models import Clothing, ImagesClothing



class ImagesClothSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImagesClothing
        fields = [
            'image',
             ]





class ClothSerializer(serializers.ModelSerializer):

    created_by_id = serializers.IntegerField(required=False)
    published_date = serializers.DateField(required = False)

    def validate_tel(self, data):
        if len(str(data)) == 10:
            return data
        else:
            raise serializers.ValidationError({"Este numero de telefono no es valido": "This phone number don't exists"})
        



    imagescloth = ImagesClothSerializer(many=True)

    

    class Meta:
        model = Clothing
        fields = [
            'id',
            'type_of_cloth',
            'size',
            'status',
            'description',
            'price',
            'tel',
            'created_by_id',
            'creation_date',
            'published_date',
            'imagescloth',
            ] 


    def create(self, validated_data):

        imagescloth_data = validated_data.pop('imagescloth')
        cloth = Clothing.objects.create(**validated_data)

        for imagecloth_data in imagescloth_data:
            ImagesClothing.objects.create(cloth=cloth, **imagecloth_data)

        return cloth 
        
    

from rest_framework import serializers

from ..models import ImagesTool, Tool


class ImagesToolSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImagesTool
        fields = [
            'image',
             ]





class ToolSerializer(serializers.ModelSerializer):

    created_by_id = serializers.IntegerField(required=False)
    published_date = serializers.DateField(required = False)

    def validate_tel(self, data):
        if len(str(data)) == 10:
            return data
        else:
            raise serializers.ValidationError({"Este numero de telefono no es valido": "This phone number don't exists"})
        



    imagestool = ImagesToolSerializer(many=True, read_only =True)
    uploaded_images = serializers.ListField(child = serializers.FileField(max_length = 1000000, allow_empty_file = False, use_url = False), write_only = True) # crea un array en donde se van a meter cosas

    

    class Meta:
        model = Tool
        fields = [
            'id',
            'tool',
            'status',
            'description',
            'price',
            'tel',
            'created_by_id',
            'creation_date',
            'published_date',
            'imagestool',
            'uploaded_images',
            ] 


    def create(self, validated_data):

        uploaded_data = validated_data.pop('uploaded_images',)
        tool = Tool.objects.create(**validated_data)

        for uploaded_item in uploaded_data:
            ImagesTool.objects.create(tool=tool, image= uploaded_item)

        return tool 
        
    











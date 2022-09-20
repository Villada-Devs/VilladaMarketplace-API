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
        



    #imagestool = ImagesToolSerializer(many=True)

    

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
            ] 


    # def create(self, validated_data):

    #     imagestool_data = validated_data.pop('imagestool')
    #     tool = Tool.objects.create(**validated_data)

    #     for imagetool_data in imagestool_data:
    #         ImagesTool.objects.create(tool=tool, **imagetool_data)

    #     return tool 
        
    











from rest_framework import serializers

from ..models import Clothing, ImagesClothing, size_clothing


class PropsNestedSerializer(serializers.Serializer):
    size = serializers.ChoiceField(size_clothing)
    description = serializers.CharField(required = False, allow_blank= True)
    
    class Meta: 
        ref_name = "props for cloth"

class ImagesClothSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImagesClothing
        fields = [
            'image',
             ]



class ClothSerializer(serializers.ModelSerializer):

    created_by_user = serializers.CharField(source="created_by.username", read_only=True)

    #created_by_id = serializers.IntegerField(required=False)
    published_date = serializers.DateField(required = False)



    def validate_tel(self, data):
        if len(str(data)) == 10:
            return data
        else:
            raise serializers.ValidationError({"Este numero de telefono no es valido": "This phone number don't exists"})
        



    product_images = ImagesClothSerializer(many=True, read_only =True)
    uploaded_images = serializers.ListField(child = serializers.ImageField(max_length = 1000000, allow_empty_file = False, use_url = False), write_only = True) # crea un array en donde se van a meter cosas
    


    props = PropsNestedSerializer(source='*')

    class Meta:
        model = Clothing
        ref_name = "Clothing"
        fields = [
            'id',
            'product_name',
            'props',
            'status',
            'price',
            'tel',
            'created_by_user',
            'creation_date',
            'published_date',
            'product_images',
            'uploaded_images',
            ] 


    def create(self, validated_data):

        uploaded_data = validated_data.pop('uploaded_images')
        cloth = Clothing.objects.create(**validated_data)

        for uploaded_item in uploaded_data:
            ImagesClothing.objects.create(cloth=cloth, image= uploaded_item)

        return cloth 




    def update(self, instance, validated_data):
        images = validated_data.pop('uploaded_images', None)

        print("imagenes nuevas: ",images)
        
        if images:
            #print(instance.id)
            images_tool_old = ImagesClothing.objects.filter(tool_id = instance.id)
            print("imagenes cloth que ya estaban: ", images_tool_old)
            images_tool_old.delete()
        

            cloth_image_model_instance = [ImagesClothing(tool=instance, image=image)for image in images]
            ImagesClothing.objects.bulk_create(cloth_image_model_instance)

        return super().update(instance, validated_data)

        
    

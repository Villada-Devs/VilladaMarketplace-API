from rest_framework import serializers

from ..models import ImagesTool, Tool


class ImagesToolSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImagesTool
        fields = [
            'image',
             ]





class ToolSerializer(serializers.ModelSerializer):

    created_by_user = serializers.CharField(source="created_by.username", read_only = True) 

    #created_by_id = serializers.IntegerField(required=False)
    published_date = serializers.DateField(required = False)

    
    # VALIDACIONES


    def validate(self, data):
        #print(data)
        if len(str(data['tel'])) == 10:
            return data                                 # esto hace lo mismo que el de arriba pero queria mostrar que despues del validate arriba si le pones el dato ya te lo trae solo a ese dato
        else:
            raise serializers.ValidationError({"tel": "This phone number don't exists"})

            
    


    imagestool = ImagesToolSerializer(many=True, read_only =True)
    uploaded_images = serializers.ListField(child = serializers.ImageField(max_length = 1000000, allow_empty_file = False, use_url = False), write_only = True) # el listField() crea un array en donde se van a meter los objetos, en este caso las imagenes

    

    class Meta:
        model = Tool
        fields = [
            'id',
            'tool',
            'status',
            'description',
            'price',
            'tel',
            'created_by_user',
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
        
    

    # 9/9/22  se pueden cambiar las imagenes y se cambian por las que estaban antes 
    # (un problema es que si quiero cambiar otra cosa que no sean las imagenes me tira error 
    # de que no puede estar vacio el campo de 'uploaded_images')



    # la diferencia de este update con el de Events es que en Events agregan imagenes nuevas y en 
    # Marketplace se cambia las nuevas por las viejas
    def update(self, instance, validated_data):
        images = validated_data.pop('uploaded_images', None)

        print("imagenes nuevas: ",images)
        
        if images:
            #print(instance.id)
            images_tool_old = ImagesTool.objects.filter(tool_id = instance.id)
            print("imagenes tools que ya estaban: ", images_tool_old)
            images_tool_old.delete()
        

            tool_image_model_instance = [ImagesTool(tool=instance, image=image)for image in images]
            ImagesTool.objects.bulk_create(tool_image_model_instance)

        return super().update(instance, validated_data)










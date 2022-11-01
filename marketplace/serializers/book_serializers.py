from rest_framework import serializers

from ..models import Book, ImagesBook


class PropsNestedSerializer(serializers.Serializer):
    author = serializers.CharField()
    subject = serializers.CharField()
    course = serializers.CharField()
    editorial = serializers.CharField()


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

    
    # def validate(self, data):
    #     if len(str(data['tel'])) == 10:
    #         return data                                 # esto hace lo mismo que el de arriba pero queria mostrar que despues del validate arriba si le pones el dato ya te lo trae solo a ese dato
    #     else:
    #         raise serializers.ValidationError({"tel": "This phone number don't exists"})

            
            

            

    created_by_user = serializers.CharField(source="created_by.username", read_only=True) # esto es para poder ver el nombre del usuario que lo creo y no el id y el read_only para que no nos lo pida en el serializer ya que se lo ponemos en el views

    #created_by_id = serializers.IntegerField(required=False) # esto era para que no me lo pida obligatoriamente en el serializer al created_by ya que se pone solo en views
    published_date = serializers.DateField(required = False)


    imagesbook = ImagesBookSerializer(many=True, read_only =True)
    uploaded_images = serializers.ListField(child = serializers.ImageField(max_length = 1000000, allow_empty_file = False, use_url = False), write_only = True) # crea un array en donde se van a meter cosas
    
    

    props = PropsNestedSerializer(source='*')

    class Meta:
        model = Book
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
            'imagesbook',
            'uploaded_images',
            ] 

    
    def create(self, validated_data):

        uploaded_data = validated_data.pop('uploaded_images')
        book = Book.objects.create(**validated_data)

        for uploaded_item in uploaded_data:
            ImagesBook.objects.create(book=book, image= uploaded_item)
        return book
    



    def update(self, instance, validated_data):
        images = validated_data.pop('uploaded_images', None)

        print("imagenes nuevas: ",images)
        
        if images:
            #print(instance.id)
            images_tool_old = ImagesBook.objects.filter(tool_id = instance.id)
            print("imagenes book que ya estaban: ", images_tool_old)
            images_tool_old.delete()
        

            book_image_model_instance = [ImagesBook(tool=instance, image=image)for image in images]
            ImagesBook.objects.bulk_create(book_image_model_instance)

        return super().update(instance, validated_data)
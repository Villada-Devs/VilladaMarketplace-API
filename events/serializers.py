
from rest_framework import serializers
from .models import Event, ImagesEvent

#UPF API
#Serializer de las imagenes, uno a muchos con un evento
class ImagesEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImagesEvent
        fields = [
            'image'
             ]

class EventsSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="created_by.username", read_only=True)
    #Campo para ver las imagenes que tiene el objeto(solo lectura)
    imagesevent = ImagesEventSerializer(many=True, read_only =True)
    #Campo para mandar imagenes al objeto(solo escritura)
    uploaded_images = serializers.ListField(child = serializers.FileField(max_length = 1000000, allow_empty_file = False, use_url = False), write_only = True)
    class Meta:
        model = Event
        fields = ['id',
        'author',
        'title', 
        'body', 
        'created_date', 
        'event_date',
        'imagesevent',
        'uploaded_images',
        ]
    
    def create(self, validated_data):
        uploaded_data = validated_data.pop('uploaded_images')
        event = Event.objects.create(**validated_data)

        for uploaded_item in uploaded_data:
            ImagesEvent.objects.create(event=event, image= uploaded_item)
        return event
    
    def clear_existing_images(self, instance):
        for event_image in instance.imagesevent.all():
            event_image.delete()


    def update(self, instance, validated_data):
        images = validated_data.pop('uploaded_images', None)
        if images:
            self.clear_existing_images(instance)
            event_image_model_instance = [ImagesEvent(event=instance, image=image)for image in images]
            ImagesEvent.objects.bulk_create(
                event_image_model_instance
            )
        return super().update(instance, validated_data)
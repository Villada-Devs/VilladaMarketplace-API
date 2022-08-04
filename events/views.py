
from .serializers import EventsSerializer
from .models import Event
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
# Create your views here.

class EventsViewSet(viewsets.ViewSet):
    """
    GET (List all events, all users can list)
    """
    def list(self, request):
        queryset = Event.objects.all()
        EventSerializer = EventsSerializer(queryset, many=True)
        return Response(EventSerializer.data)

    """
    POST (Create event only admin can post)
    """   
    def post(self, request):
        user_state = request.user.is_staff
        if user_state == True:
            serializer = EventsSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save(created_by = self.request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error' : 'Authorization Required'}, status=status.HTTP_401_UNAUTHORIZED)
    
class EventsDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = EventsSerializer
    lookup_field =  "id"
    
    def get_queryset(self):
        return Event.objects.filter()

    """
    DELETE (delete an event passing ID, only admin can delete)
    """
    def destroy(self, request, *args, **kwargs):
        user_state = request.user.is_staff
        if user_state == True:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'ok' : 'Event deleted succesfully'},status=status.HTTP_200_OK)
        else:
            return Response({'error' : 'Authorization Required'}, status=status.HTTP_401_UNAUTHORIZED)

    """
    PATCH (update an event passing ID, only admin can delete)
    """
    def update(self, request, *args, **kwargs):
        user_state = request.user.is_staff
        if user_state == True:
            return super().update(request, *args, **kwargs)

        else:
            return Response({'error' : 'Authorization Required'}, status=status.HTTP_401_UNAUTHORIZED)





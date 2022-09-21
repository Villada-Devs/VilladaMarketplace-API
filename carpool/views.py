from .serializers import poolsSerializer
from .models import Pool
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.generics import RetrieveUpdateDestroyAPIView

# Create your views here.

class poolsListView(viewsets.ViewSet):

    """
    LIST (retrieve a list of all pools, if a user id is sent in the url retrieve user pools list)
    """
    def list(self, request):
        # PAGINATION
        page = request.query_params.get('page')
        
        if page == None:
            queryset = Pool.objects.all()[:15]
            
        else:
            page = int(page)
            page = page +1

            max = page * 15
            min = max -15
            queryset = Pool.objects.all()[min:max]


        user = request.GET.get('created_by')
        
        if user:
            if str(request.user.id) != user:
                print(request.user.id, user)
                return Response({'error' : 'You can not see the pool list from other user'}, status=status.HTTP_401_UNAUTHORIZED)
            queryset = queryset.filter(created_by=user)
        
        serializer = poolsSerializer(queryset, many=True)
        return Response(serializer.data)

    """
    POST (create a carpool entry)
    """

    def post(self, request):
        serializer = poolsSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(created_by = self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    DELETE (delete a pool sending the id in the url, the user only can delete her own pools)
    """
    def delete(self, request, *args, **kwargs): 
        pool_id = request.query_params.get('id')
        if not pool_id:
            return Response({'error' : 'You need to send pool id in the url'}, status=status.HTTP_403_FORBIDDEN)
        
        if not Pool.objects.filter(id=pool_id).exists():
            return Response({'error' : 'There is not a pool with this id'}, status=status.HTTP_403_FORBIDDEN)
        
        

        if instance.created_by != self.request.user:
            return Response({'error' : 'You are not the owner of this pool'}, status=status.HTTP_401_UNAUTHORIZED)
            
        instance = Pool.objects.filter(id=pool_id).last()
        instance.delete()
        return Response({'ok' : 'Pool deleted succesfully'}, status=status.HTTP_200_OK)
    

    #CODING (UPDATE )
    def update(self, request, *args, **kwargs):
        pool_id= request.query_params.get('id')
        instance = self.get_object()
        print(instance)



class PoolsDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = poolsSerializer
    lookup_field =  "id"
    
    def get_queryset(self):
        return Pool.objects.filter()

    """
    DELETE (delete an event passing ID, only admin can delete)
    """
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance.created_by)
        print(self.request.user)
        if self.request.user != instance.created_by:
            self.perform_destroy(instance)
            return Response({'error' : 'You are not the owner of this pool'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            self.perform_destroy(instance)
            return Response({'ok' : 'Event deleted succesfully'},status=status.HTTP_200_OK)

    """
    PATCH (update an event passing ID, only admin can edit)
    """
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.request.user == instance.created_by:
            return super().update(request, *args, **kwargs)
        else:
            return Response({'error' : 'You are not the owner of this pool'}, status=status.HTTP_401_UNAUTHORIZED)





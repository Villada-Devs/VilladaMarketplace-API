from datetime import datetime, timedelta
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from ..serializers.cloth_serializers import ClothSerializer


class ClothViewSet(viewsets.ModelViewSet):
    serializer_class = ClothSerializer

    def get_queryset(self, pk=None):
        
        date = datetime.now() - timedelta(weeks=2)
        
        # si tiene mas de dos semanas la publicacion se pone "on_circulation" = False
        self.serializer_class().Meta.model.objects.filter(creation_date__lte =date).update(on_circulation = False)
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(on_circulation = True)
        else:
            return self.get_serializer().Meta.model.objects.filter(id = pk, on_circulation = True).first() 




    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)   




    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by = self.request.user) #pone automaticamente cuando se crea el que creo el post y se exluye en el serializer el "created_by"
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)    


    def update(self, request, *args, **kwargs):

        partial = kwargs.pop('partial', False)
        if request.user == self.get_object().created_by:

            instance = self.get_object()    
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        else:
            return Response({'Error':'You are not authorized to edit this product'}, status = status.HTTP_401_UNAUTHORIZED)


    def destroy(self, request, pk=None):
        cloth = self.get_queryset().filter(id = pk).first()

        if cloth != None:
            if request.user ==self.get_object().created_by:

                cloth.on_circulation = False
                cloth.save()
                return Response({'Message':'The cloth was delete correctly'}, status = status.HTTP_200_OK)
            else:
                return Response({'Error':'You are not authorized to delete this product'}, status = status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'Error':"This product don't exists"}, status = status.HTTP_400_BAD_REQUEST)





"""
class ClothListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ClothSerializer

    def get_queryset(self):
        return ClothSerializer.Meta.model.objects.filter(on_circulation = True)

    def post(self, request):
        # enviando info al serializer
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Producto creado correctamente!'}, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)





class ClothRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClothSerializer


    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(on_circulation = True)
        else:
            return self.get_serializer().Meta.model.objects.filter(id = pk, on_circulation = True).first() 
  
# arriba estamos diciendo que si el pk es None solamente traiga los que estan en circulacion despues abajo saltara error por no tener pk por que se necesita uno


    def patch(self, request, pk=None):
        if self.get_queryset(pk):
            cloth_serializer = self.serializer_class(self.get_queryset(pk)) # le pasamos un pk para elegir un solo objeto en especial y serializarlo
            return Response(cloth_serializer.data, status = status.HTTP_200_OK)
        else:
            return Response({'error': 'No existe libro con esa pk'}, status = status.HTTP_400_BAD_REQUEST)



    def put(self, request, pk=None):
        if self.get_queryset(pk):
            cloth_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if cloth_serializer.is_valid():
                cloth_serializer.save()
                return Response(cloth_serializer.data, status = status.HTTP_200_OK)
            else:
                return Response(cloth_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, pk=None):
        cloth = self.get_queryset().filter(id = pk).first()

        if cloth:
            cloth.on_circulation = False
            cloth.save()
            return Response({'message':'Ropa eliminada correctamente'}, status = status.HTTP_200_OK)
        else:
            return Response({'error':'No existe esa ropa'}, status = status.HTTP_400_BAD_REQUEST)
"""
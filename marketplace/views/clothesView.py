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

 

    def destroy(self, request, pk=None):
        cloth = self.get_queryset().filter(id = pk).first()

        if cloth != None:
            cloth.on_circulation = False
            cloth.save()
            return Response({'message':'Ropa eliminado correctamente'}, status = status.HTTP_200_OK)
        else:
            return Response({'error':'No existe ese producto'}, status = status.HTTP_400_BAD_REQUEST)







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
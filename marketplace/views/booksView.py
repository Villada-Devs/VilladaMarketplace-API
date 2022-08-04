from datetime import datetime, timedelta
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from ..serializers.book_serializers import BookSerializer

from ..models import *


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer

    def get_queryset(self, pk=None):
        
        date = datetime.now() - timedelta(weeks=2)
        
        # si tiene mas de dos semanas la publicacion se pone "on_circulation" = False
        self.serializer_class().Meta.model.objects.filter(creation_date__lte =date).update(on_circulation = False)

        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(on_circulation = True)
        else:
            return self.get_serializer().Meta.model.objects.filter(id = pk, on_circulation = True).first() 

 
# estos metodos ya estan definidos en la clase ModelViewSet por lo unico que los redefinimos es por que vamos a hacer algo diferente como por ejemplo con destroy no queremos borrar la instancia solo queremos cambiar el "on_circulation" a False
# https://www.cdrf.co/3.13/rest_framework.viewsets/ModelViewSet.html

    def list(self, request):

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)  



    def destroy(self, request, pk=None):
        libro = self.get_queryset().filter(id = pk).first()

        if libro != None:
            libro.on_circulation = False
            libro.save()
            return Response({'message':'Libro eliminado correctamente'}, status = status.HTTP_200_OK)
        else:
            return Response({'error':'No existe ese producto'}, status = status.HTTP_400_BAD_REQUEST)




# esta forma es cuando NO trabajamos con viewsets ni routers

"""


class BookListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        return BookSerializer.Meta.model.objects.filter(on_circulation = True)

    def post(self, request):
        # enviando info al serializer
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            serializer.save()
            print("se creo un libro pa")
            return Response({'message':'Producto creado correctamente!'}, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    




class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer


    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(on_circulation = True)
        else:
            return self.get_serializer().Meta.model.objects.filter(id = pk, on_circulation = True).first() 
  
# arriba estamos diciendo que si el pk es None solamente traiga los que estan en circulacion despues abajo saltara error por no tener pk por que se necesita uno


    def patch(self, request, pk=None):
        if self.get_queryset(pk):
            book_serializer = self.serializer_class(self.get_queryset(pk)) # le pasamos un pk para elegir un solo objeto en especial y serializarlo
            return Response(book_serializer.data, status = status.HTTP_200_OK)
        else:
            return Response({'error': 'No existe libro con esa pk'}, status = status.HTTP_400_BAD_REQUEST)



    def put(self, request, pk=None):
        if self.get_queryset(pk):
            book_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if book_serializer.is_valid():
                book_serializer.save()
                return Response(book_serializer.data, status = status.HTTP_200_OK)
            else:
                return Response(book_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, pk=None):
        libro = self.get_queryset().filter(id = pk).first()

        if libro:
            libro.on_circulation = False
            libro.save()
            return Response({'message':'Libro eliminado correctamente'}, status = status.HTTP_200_OK)
        else:
            return Response({'error':'No existe ese libro'}, status = status.HTTP_400_BAD_REQUEST)
"""
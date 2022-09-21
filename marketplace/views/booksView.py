from datetime import datetime, timedelta, date
from marketplace.pagination import CustomPageNumberPagination
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response

from ..serializers.book_serializers import BookSerializer

from ..models import *

from ..pagination import CustomPageNumberPagination

class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'course', 'subject'] # filtros de busqueda, (.../?search=)

    pagination_class = CustomPageNumberPagination

    def get_queryset(self, pk=None):
        
        date = datetime.now() - timedelta(weeks=3)
        print(date)
        
    
        
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(checked = True, published_date__gte =date) # trae todos los books que esten 'checked' = True y los que tengan 'published_date' por arriba de la fecha (date)
        else:
            return self.get_serializer().Meta.model.objects.filter(id = pk, checked = True, published_date__gte =date).first() 

 


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
        libro = self.get_queryset().filter(id = pk).first()

        if libro != None:
            if request.user ==self.get_object().created_by:

                libro.delete()
                return Response({'Message':'Book deleted correctly'}, status = status.HTTP_200_OK)
            else:
                return Response({'Error':'You are not authorized to delete this product'}, status = status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"Error': 'This product don't exists"}, status = status.HTTP_400_BAD_REQUEST)





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
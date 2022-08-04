from datetime import datetime, timedelta
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from drf_multiple_model.viewsets import ObjectMultipleModelAPIViewSet

from ..models import Book, Clothing, Tool

from ..serializers.book_serializers import BookSerializer
from ..serializers.cloth_serializers import ClothSerializer
from ..serializers.tool_serializers import ToolSerializer



class MyPostsViewset(ObjectMultipleModelAPIViewSet):
    
    def get_querylist(self):
        
        date = datetime.now() - timedelta(weeks=2)
        
        # si tiene mas de dos semanas la publicacion se pone "on_circulation" = False
        BookSerializer.Meta.model.objects.filter(creation_date__lte =date).update(on_circulation = False)
        ClothSerializer.Meta.model.objects.filter(creation_date__lte =date).update(on_circulation = False)
        ToolSerializer.Meta.model.objects.filter(creation_date__lte =date).update(on_circulation = False)

        user_id=self.request.GET.get('user', self.request.user.id) # https:.../?user=(id de usuario)
        #print(user_id)
        querylist = [
            {'queryset': Book.objects.filter(on_circulation = True, created_by_id = user_id), 'serializer_class': BookSerializer },
            {'queryset': Clothing.objects.filter(on_circulation = True, created_by_id = user_id), 'serializer_class': ClothSerializer},
            {'queryset': Tool.objects.filter(on_circulation = True, created_by_id = user_id), 'serializer_class': ToolSerializer},
        ]
        return querylist



"""
print("#################################################################################")
print("")
libros = Book.objects.filter(on_circulation = True)
clothes = Clothing.objects.filter(on_circulation = True)
tools = Tool.objects.filter(on_circulation = True)

print(list(chain(libros, clothes, tools)))
"""
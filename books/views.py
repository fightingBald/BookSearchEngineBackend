from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from .search import *
# Create your views here.

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    def get_queryset(self):
        q = self.request.query_params.get('q')
        if q:
            return search_by_keyword(q)
        return super().get_queryset()



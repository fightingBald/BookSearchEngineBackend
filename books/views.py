from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from .search import search_by_keyword , search_by_regex, search_by_suggestion
# Create your views here.

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    def get_queryset(self):
        q = self.request.query_params.get('q')
        if q:
            return search_by_keyword(q)

        regex = self.request.query_params.get('regex')
        if regex:
            return search_by_regex(regex)

        return super().get_queryset()


class BookSuggestionView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    def get_queryset(self):
        book_id = self.request.query_params.get('book_id')
        if book_id:
            return search_by_suggestion(book_id)
        return super().get_queryset()

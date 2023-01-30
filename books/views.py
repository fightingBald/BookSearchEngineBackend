from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .kmp import KMPSearch
from .ahoullman import Ahoullman
from .models import Book
from .serializers import BookSerializer
from .search import search_by_keyword , search_by_regex, search_by_suggestion

import logging.config

logging.config.fileConfig('logging.conf')
# create logger
logger = logging.getLogger('daarlogger')
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




class SearchView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    def get_queryset(self):
        q = self.request.query_params.get('q')
        if q:
            results = []
            for book in Book.objects.all():
                occurence = KMPSearch(q, book.text)
                if occurence:
                    results.append((book, occurence))
            results.sort(key=lambda x: x[1], reverse=True)
            return [book for book, _ in results]
        regex = self.request.query_params.get('regex')
        if regex:
            results = []
            for book in Book.objects.all():
                sol = Ahoullman()
                occurence = sol.occurences_that_match_pattern(regex, book.text)
                if occurence:
                    results.append((book, occurence))
            results.sort(key=lambda x: x[1], reverse=True)
            return [book for book, _ in results]

        return super().get_queryset()






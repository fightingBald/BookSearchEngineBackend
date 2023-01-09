# _*_ coding : utf-8 _ * _ 
# @Time : 09/01/2023 12:46
# @Author : Huayi TANG
# File : documents.py
# @Project : searchEngine

from django_elasticsearch_dsl import Index , Document

from .models import Book

# Name of the Elasticsearch index
books = Index('books')
# See Elasticsearch Indices API reference for available settings
books.settings(number_of_shards=1, number_of_replicas=0)

@books.doc_type #Decorator
class BookDocument(Document):#Class
    # The fields of the model you want to be indexed in Elasticsearch
    class Django:#Class
        model = Book# The model associated with this Document
        fields = [# The fields of the model you want to be indexed in Elasticsearch
            'title',
            'author',
            'link',
            'bookshelf',
            'text',
        ]








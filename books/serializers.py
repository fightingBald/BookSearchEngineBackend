# _*_ coding : utf-8 _ * _ 
# @Time : 10/01/2023 01:15
# @Author : Huayi TANG
# File : serializers.py
# @Project : searchEngine

from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

# Path: books/urls.py






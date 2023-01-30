from django.db import models

#PATH: books/models.py
from pyexcel import get_sheet
from django.db import models

#Create a model for gutenberg_data.csv

class Book(models.Model):
    #Title, Author, Link, ID, Bookshelf, Text
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    link = models.URLField()
    #book_id = models.IntegerField()
    bookshelf = models.CharField(max_length=200)
    text = models.TextField()

    def __str__(self):
        return f"{self.title} by {self.author}"

    @classmethod
    def populate(cls):
        sheet = get_sheet(file_name="gutenberg_data.csv")
        for row in sheet:
            book = cls(title=row[0], author=row[1], link=row[2], bookshelf=row[4], text=row[5])
            book.save()


'''
    @classmethod
    def search_by_keyword(cls, keyword):
        return cls.objects.filter(title__icontains=keyword) | cls.objects.filter(author__icontains=keyword) | cls.objects.filter(bookshelf__icontains=keyword) | cls.objects.filter(text__icontains=keyword)

'''








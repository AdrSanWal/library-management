from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from . import serializers
from core.models import Book, Author, Category, Serie


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer

    def get_queryset(self):
        """Return all Books except if there are query parameters"""
        request = self.request.GET
        if 'title' in request:
            return Book.objects.filter(title__icontains=request['title'])
        if 'serie' in request:
            return Book.objects.filter(serie=request['serie'])
        if 'author' in request:
            return Book.objects.filter(author=request['author'])
        if 'category' in request:
            return Book.objects.filter(categories=request['category'])
        if 'available' in request:
            return Book.objects.filter(available=request['available'])
        return self.queryset


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = serializers.AuthorSerializer

    def get_queryset(self):
        """Return all Authors except if there is q in the parameters"""
        request = self.request.GET
        if 'q' in request:
            return Author.objects.filter(full_name__icontains=request['q'])
        return self.queryset


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        """Return all Categories except if there is q in the parameters"""
        request = self.request.GET
        if 'q' in request:
            return Category.objects.filter(name__icontains=request['q'])
        return self.queryset


class SerieViewSet(ModelViewSet):
    queryset = Serie.objects.all()
    serializer_class = serializers.SerieSerializer

    def get_queryset(self):
        """Return all Series except if there is q in the parameters"""
        request = self.request.GET
        if 'q' in request:
            return Serie.objects.filter(name__icontains=request['q'])
        return self.queryset

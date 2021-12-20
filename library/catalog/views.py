from rest_framework.viewsets import ModelViewSet

from . import serializers
from core.models import Book, Author, Category, Serie


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = serializers.AuthorSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class SerieViewSet(ModelViewSet):
    queryset = Serie.objects.all()
    serializer_class = serializers.SerieSerializer
